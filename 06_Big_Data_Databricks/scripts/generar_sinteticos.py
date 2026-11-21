#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de datos sintéticos para la etapa Databricks (EXP-02)
Proyecto: Sistema automatizado para el monitoreo de empleados - BASAV Grupo 2

Qué hace
--------
1. Lee las exportaciones CSV de las tablas Asistencia y Tareas de A&SG_OLTP
   (582 + 582 filas). Solo conserva las columnas de la guía; si el CSV trae
   nombres, correos, teléfonos o PIN, esas columnas se descartan y se avisa.
2. Normaliza el conjunto base y lo guarda como asistencias_base.csv y
   tareas_base.csv (mismas filas, fechas en formato ISO, UTF-8, separador coma).
3. Amplía el conjunto con trabajadores sintéticos (IDs desde 1001) hasta llegar
   exactamente a cada escala pedida (por defecto 5 000 y 10 000 filas por tabla).
   Cada escala contiene el conjunto base completo + filas sintéticas, y la de
   10 000 incluye a la de 5 000 (misma semilla, mismo orden).
4. Valida las reglas y escribe un manifiesto con filas, bytes, SHA-256, semilla
   y los KPI (TPA, ICT, TDT, IEP) de cada archivo.

Regla de generación (para declarar en 4.2 / 5.7)
------------------------------------------------
- Cada trabajador sintético toma como plantilla a un trabajador real del
  conjunto base (elegido al azar con la semilla).
- Asistencia: copia las fechas de la plantilla (así se mantiene una sola fila
  por trabajador y por día). La hora de entrada se toma al azar de las entradas
  de la plantilla y se le suma un desfase uniforme de ±5 minutos. Salida a las
  18:00 del mismo día. Estado: "A tiempo" si la entrada es antes de 09:41:00,
  "Tardanza" si es 09:41:00 o después.
- Tareas: copia las tareas de la plantilla (proyecto, Fecha, Fecha_Inicio). Con
  probabilidad 0,30 toma de otra tarea base al azar el bloque
  Estado_Tarea + Observaciones + plazo (Fecha_Entrega - Fecha_Inicio).
  Estado_Tarea solo puede ser "Completada", "En Progreso" o "Asignada"; la marca
  "[ENTREGADO FUERA DE PLAZO]" viaja en Observaciones.
- Los IDs de trabajador sintéticos (1001, 1002, ...) no existen en la tabla
  Trabajadores del OLTP: son etiquetas para la prueba de volumen.

Uso
---
    python generar_sinteticos.py --asistencia Asistencia.csv --tareas Tareas.csv
    python generar_sinteticos.py --asistencia A.csv --tareas T.csv --semilla 2026 \
        --escalas 5000 10000 --salida datos_databricks

Solo usa la biblioteca estándar de Python 3.8+ (no necesita pandas).
"""

import argparse
import csv
import hashlib
import io
import json
import random
import sys
from datetime import datetime, date, time, timedelta
from pathlib import Path

VERSION = "1.0"

COLS_ASIS = ["ID_Asistencia", "ID_Trabajador", "Fecha_Entrada", "Fecha_Salida",
             "Fecha_Calculada", "Estado_Asistencia"]
COLS_TAREA = ["ID_Tarea", "ID_Trabajador", "ID_Proyecto", "Fecha", "Fecha_Inicio",
              "Fecha_Entrega", "Estado_Tarea", "Observaciones"]
FECHAS_ASIS = ["Fecha_Entrada", "Fecha_Salida", "Fecha_Calculada"]
FECHAS_TAREA = ["Fecha", "Fecha_Inicio", "Fecha_Entrega"]

ESTADOS_TAREA = ["Completada", "En Progreso", "Asignada"]
MARCA_FUERA_PLAZO = "[ENTREGADO FUERA DE PLAZO]"
LIMITE_PUNTUAL = time(9, 41, 0)       # antes de 09:41:00 = A tiempo
HORA_SALIDA = time(18, 0, 0)
DESFASE_SEG = 300                     # ±5 minutos
PROB_VARIACION_TAREA = 0.30
PRIMER_ID_SINTETICO = 1001
PALABRAS_SENSIBLES = ("nombre", "apellido", "correo", "email", "mail",
                      "telefono", "teléfono", "celular", "pin", "dni", "clave",
                      "password", "contrasena", "contraseña")

FORMATOS_FECHA = [
    "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d",
    "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y",
    "%Y/%m/%d %H:%M:%S", "%Y/%m/%d",
]
VACIOS = {"", "null", "none", "nan", "nat"}


# --------------------------------------------------------------------------
# Lectura y normalización
# --------------------------------------------------------------------------
def leer_csv(ruta, columnas, nombre_tabla):
    datos = Path(ruta).read_bytes()
    for codificacion in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = datos.decode(codificacion)
            break
        except UnicodeDecodeError:
            continue
    muestra = texto[:5000]
    try:
        dialecto = csv.Sniffer().sniff(muestra, delimiters=",;\t|")
        delim = dialecto.delimiter
    except csv.Error:
        delim = ","
    lector = csv.DictReader(io.StringIO(texto), delimiter=delim)
    if lector.fieldnames is None:
        sys.exit(f"[ERROR] {ruta} está vacío.")

    mapa = {c.strip().lower(): c for c in lector.fieldnames}
    faltan = [c for c in columnas if c.lower() not in mapa]
    if faltan:
        sys.exit(f"[ERROR] En {ruta} ({nombre_tabla}) faltan columnas: {faltan}\n"
                 f"        Columnas encontradas: {lector.fieldnames}")
    extra = [c for c in lector.fieldnames if c.strip().lower() not in
             {x.lower() for x in columnas}]
    sensibles = [c for c in extra if any(p in c.lower() for p in PALABRAS_SENSIBLES)]
    if sensibles:
        print(f"[AVISO] {nombre_tabla}: se descartan columnas con datos personales: {sensibles}")
    otras = [c for c in extra if c not in sensibles]
    if otras:
        print(f"[INFO]  {nombre_tabla}: columnas no usadas y descartadas: {otras}")

    filas = []
    for r in lector:
        filas.append({c: (r[mapa[c.lower()]] or "").strip() for c in columnas})
    return filas


def parse_fecha(valor):
    if valor is None or valor.strip().lower() in VACIOS:
        return None
    v = valor.strip()
    for fmt in FORMATOS_FECHA:
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    # SQL Server a veces exporta 7 decimales: recortar a 6
    if "." in v:
        base, frac = v.split(".", 1)
        try:
            return datetime.strptime(f"{base}.{frac[:6]}", "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            pass
    raise ValueError(f"Formato de fecha no reconocido: {valor!r}")


def texto_o_vacio(v):
    return "" if v is None or v.strip().lower() in VACIOS else v.strip()


def preparar(filas, cols_fecha, cols_id):
    for r in filas:
        for c in cols_id:
            try:
                r[c] = int(float(r[c]))
            except ValueError:
                sys.exit(f"[ERROR] {c} no es numérico: {r[c]!r}")
        for c in cols_fecha:
            r[c] = parse_fecha(r[c])
    # ¿la columna lleva hora? (si todas las horas son 00:00:00 se escribe solo fecha)
    con_hora = {c: any(r[c] is not None and r[c].time() != time(0) for r in filas)
                for c in cols_fecha}
    return con_hora


def fmt_fecha(v, con_hora):
    if v is None:
        return ""
    return v.strftime("%Y-%m-%d %H:%M:%S") if con_hora else v.strftime("%Y-%m-%d")


# --------------------------------------------------------------------------
# Reglas y KPI
# --------------------------------------------------------------------------
def estado_por_hora(entrada, txt_a_tiempo, txt_tardanza):
    return txt_a_tiempo if entrada.time() < LIMITE_PUNTUAL else txt_tardanza


def kpis(asis, tareas):
    n_a = len(asis)
    a_tiempo = sum(1 for r in asis if r["Estado_Asistencia"].lower() == "a tiempo")
    n_t = len(tareas)
    sin_obs = sum(1 for r in tareas if r["Estado_Tarea"].lower() == "completada"
                  and texto_o_vacio(r["Observaciones"]) == "")
    fuera = sum(1 for r in tareas if "FUERA DE PLAZO" in r["Observaciones"].upper())
    tpa = 100.0 * a_tiempo / n_a if n_a else None
    ict = 100.0 * sin_obs / n_t if n_t else None
    tdt = 100.0 * fuera / n_t if n_t else None
    iep = (tpa * 0.30 + ict * 0.50 + (100 - tdt) * 0.20) if None not in (tpa, ict, tdt) else None
    return {"asistencias": n_a, "a_tiempo": a_tiempo, "tareas": n_t,
            "completadas_sin_obs": sin_obs, "fuera_plazo": fuera,
            "TPA": round(tpa, 2), "ICT": round(ict, 2), "TDT": round(tdt, 2),
            "IEP": round(iep, 2)}


def validar(asis, tareas, n_esperado, txt_a_tiempo, txt_tardanza, ids_base_asis):
    errores = []
    if n_esperado is not None:
        if len(asis) != n_esperado:
            errores.append(f"Asistencia tiene {len(asis)} filas, se esperaban {n_esperado}")
        if len(tareas) != n_esperado:
            errores.append(f"Tareas tiene {len(tareas)} filas, se esperaban {n_esperado}")
    # Una fila por trabajador y día
    vistos = set()
    duplicados = 0
    for r in asis:
        clave = (r["ID_Trabajador"], r["Fecha_Entrada"].date() if r["Fecha_Entrada"] else None)
        if clave in vistos:
            duplicados += 1
        vistos.add(clave)
    if duplicados:
        errores.append(f"{duplicados} filas repiten trabajador + día en Asistencia")
    # IDs únicos
    if len({r["ID_Asistencia"] for r in asis}) != len(asis):
        errores.append("ID_Asistencia repetido")
    if len({r["ID_Tarea"] for r in tareas}) != len(tareas):
        errores.append("ID_Tarea repetido")
    # Estados
    malos_t = {r["Estado_Tarea"] for r in tareas
               if r["Estado_Tarea"].lower() not in {e.lower() for e in ESTADOS_TAREA}}
    if malos_t:
        errores.append(f"Estado_Tarea fuera de catálogo: {sorted(malos_t)}")
    # Regla 09:41 y salida 18:00 (solo filas sintéticas; la base no se modifica)
    regla = 0
    salida = 0
    for r in asis:
        if r["ID_Asistencia"] in ids_base_asis:
            continue
        if r["Estado_Asistencia"] != estado_por_hora(r["Fecha_Entrada"], txt_a_tiempo, txt_tardanza):
            regla += 1
        if r["Fecha_Salida"].time() != HORA_SALIDA or r["Fecha_Salida"].date() != r["Fecha_Entrada"].date():
            salida += 1
    if regla:
        errores.append(f"{regla} filas sintéticas no cumplen la regla de 09:41:00")
    if salida:
        errores.append(f"{salida} filas sintéticas sin salida a las 18:00 del mismo día")
    return errores


# --------------------------------------------------------------------------
# Generación
# --------------------------------------------------------------------------
def variante(valores, canonico):
    """Devuelve la escritura usada en la base (p. ej. 'A tiempo' o 'A Tiempo')."""
    cand = [v for v in valores if v.lower() == canonico.lower()]
    return max(set(cand), key=cand.count) if cand else canonico


def generar(asis_base, tareas_base, objetivo_asis, objetivo_tareas, semilla,
            txt_a_tiempo, txt_tardanza, modo_calculada):
    rng = random.Random(semilla)
    asis_por_trab, tareas_por_trab = {}, {}
    for r in asis_base:
        asis_por_trab.setdefault(r["ID_Trabajador"], []).append(r)
    for r in tareas_base:
        tareas_por_trab.setdefault(r["ID_Trabajador"], []).append(r)
    plantillas = sorted(set(asis_por_trab) | set(tareas_por_trab))

    sig_asis = max(r["ID_Asistencia"] for r in asis_base) + 1
    sig_tarea = max(r["ID_Tarea"] for r in tareas_base) + 1
    sig_trab = max(PRIMER_ID_SINTETICO, max(plantillas) + 1)

    syn_a, syn_t, mapa_plantilla = [], [], []
    while len(syn_a) < objetivo_asis or len(syn_t) < objetivo_tareas:
        plantilla = rng.choice(plantillas)
        trab = sig_trab
        sig_trab += 1
        mapa_plantilla.append((trab, plantilla))

        filas_a = sorted(asis_por_trab.get(plantilla, []), key=lambda r: r["Fecha_Entrada"])
        horas = [r["Fecha_Entrada"].time() for r in filas_a if r["Fecha_Entrada"]]
        for r in filas_a:
            dia = r["Fecha_Entrada"].date()
            h = rng.choice(horas)
            seg = h.hour * 3600 + h.minute * 60 + h.second + rng.randint(-DESFASE_SEG, DESFASE_SEG)
            seg = min(max(seg, 7 * 3600), 11 * 3600 + 59 * 60 + 59)
            entrada = datetime.combine(dia, time(seg // 3600, (seg % 3600) // 60, seg % 60))
            if modo_calculada == "igual_entrada":
                calculada = entrada
            elif modo_calculada == "dia_entrada":
                calculada = datetime.combine(dia, time(0))
            else:
                calculada = r["Fecha_Calculada"]
            syn_a.append({
                "ID_Asistencia": sig_asis, "ID_Trabajador": trab,
                "Fecha_Entrada": entrada,
                "Fecha_Salida": datetime.combine(dia, HORA_SALIDA),
                "Fecha_Calculada": calculada,
                "Estado_Asistencia": estado_por_hora(entrada, txt_a_tiempo, txt_tardanza),
            })
            sig_asis += 1

        for r in sorted(tareas_por_trab.get(plantilla, []), key=lambda r: r["ID_Tarea"]):
            nueva = dict(r)
            nueva["ID_Tarea"] = sig_tarea
            nueva["ID_Trabajador"] = trab
            if rng.random() < PROB_VARIACION_TAREA:
                donante = rng.choice(tareas_base)
                nueva["Estado_Tarea"] = donante["Estado_Tarea"]
                nueva["Observaciones"] = donante["Observaciones"]
                if donante["Fecha_Entrega"] and donante["Fecha_Inicio"] and nueva["Fecha_Inicio"]:
                    nueva["Fecha_Entrega"] = nueva["Fecha_Inicio"] + (donante["Fecha_Entrega"] - donante["Fecha_Inicio"])
                elif donante["Fecha_Entrega"] is None:
                    nueva["Fecha_Entrega"] = None
            syn_t.append(nueva)
            sig_tarea += 1
    return syn_a, syn_t, mapa_plantilla


def detectar_modo_calculada(asis):
    """Cómo se relaciona Fecha_Calculada con Fecha_Entrada en la base."""
    pares = [(r["Fecha_Entrada"], r["Fecha_Calculada"]) for r in asis
             if r["Fecha_Entrada"] and r["Fecha_Calculada"]]
    if not pares:
        return "copiar"
    if all(e == c for e, c in pares):
        return "igual_entrada"
    if all(c.date() == e.date() and c.time() == time(0) for e, c in pares):
        return "dia_entrada"
    return "copiar"


# --------------------------------------------------------------------------
# Escritura
# --------------------------------------------------------------------------
def escribir(ruta, filas, columnas, cols_fecha, con_hora):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(columnas)
        for r in filas:
            fila = []
            for c in columnas:
                v = r[c]
                if c in cols_fecha:
                    fila.append(fmt_fecha(v, con_hora[c]))
                else:
                    fila.append("" if v is None else v)
            w.writerow(fila)


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 16), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description="Genera los CSV base, 5 000 y 10 000 para Databricks.")
    p.add_argument("--asistencia", required=True, help="CSV exportado de la tabla Asistencia")
    p.add_argument("--tareas", required=True, help="CSV exportado de la tabla Tareas")
    p.add_argument("--salida", default="datos_databricks", help="Carpeta de salida")
    p.add_argument("--semilla", type=int, default=2026)
    p.add_argument("--escalas", type=int, nargs="+", default=[5000, 10000])
    a = p.parse_args()

    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    asis = leer_csv(a.asistencia, COLS_ASIS, "Asistencia")
    tareas = leer_csv(a.tareas, COLS_TAREA, "Tareas")
    hora_a = preparar(asis, FECHAS_ASIS, ["ID_Asistencia", "ID_Trabajador"])
    hora_t = preparar(tareas, FECHAS_TAREA, ["ID_Tarea", "ID_Trabajador", "ID_Proyecto"])
    hora_a["Fecha_Entrada"] = hora_a["Fecha_Salida"] = True
    for r in tareas:
        r["Observaciones"] = texto_o_vacio(r["Observaciones"])
    if any(r["Fecha_Entrada"] is None for r in asis):
        sys.exit("[ERROR] Hay asistencias sin Fecha_Entrada; revisar la exportación.")

    asis.sort(key=lambda r: r["ID_Asistencia"])
    tareas.sort(key=lambda r: r["ID_Tarea"])
    n_a, n_t = len(asis), len(tareas)
    print(f"[OK]    Base leída: {n_a} asistencias, {n_t} tareas, "
          f"{len({r['ID_Trabajador'] for r in asis})} trabajadores.")

    txt_at = variante([r["Estado_Asistencia"] for r in asis], "A tiempo")
    txt_ta = variante([r["Estado_Asistencia"] for r in asis], "Tardanza")
    modo_calc = detectar_modo_calculada(asis)
    if modo_calc == "dia_entrada":
        hora_a["Fecha_Calculada"] = False

    # Revisión de la base (no se modifica, solo se informa)
    ids_base = {r["ID_Asistencia"] for r in asis}
    incoherentes = sum(1 for r in asis if r["Estado_Asistencia"].lower() in ("a tiempo", "tardanza")
                       and r["Estado_Asistencia"].lower() != estado_por_hora(r["Fecha_Entrada"], "a tiempo", "tardanza"))
    if incoherentes:
        print(f"[AVISO] Base: {incoherentes} asistencias con estado distinto a la regla de 09:41:00 "
              f"(se conservan tal cual).")
    errores_base = validar(asis, tareas, None, txt_at, txt_ta, ids_base)
    for e in errores_base:
        print(f"[AVISO] Base: {e}")

    escalas = sorted(set(a.escalas))
    if escalas[0] <= max(n_a, n_t):
        sys.exit(f"[ERROR] Cada escala debe ser mayor que la base ({max(n_a, n_t)} filas).")
    syn_a, syn_t, mapa = generar(asis, tareas, escalas[-1] - n_a, escalas[-1] - n_t,
                                 a.semilla, txt_at, txt_ta, modo_calc)

    conjuntos = [("base", asis, tareas, None)]
    for n in escalas:
        conjuntos.append((str(n), asis + syn_a[:n - n_a], tareas + syn_t[:n - n_t], n))

    manifiesto = []
    hubo_error = False
    for etiqueta, A, T, n in conjuntos:
        errores = validar(A, T, n, txt_at, txt_ta, ids_base) if n else []
        for e in errores:
            print(f"[ERROR] Escala {etiqueta}: {e}")
            hubo_error = True
        ind = kpis(A, T)
        for tabla, filas, cols, cfe, ch, nombre in (
                ("Asistencia", A, COLS_ASIS, FECHAS_ASIS, hora_a, f"asistencias_{etiqueta}.csv"),
                ("Tareas", T, COLS_TAREA, FECHAS_TAREA, hora_t, f"tareas_{etiqueta}.csv")):
            ruta = salida / nombre
            escribir(ruta, filas, cols, cfe, ch)
            base_n = n_a if tabla == "Asistencia" else n_t
            manifiesto.append({
                "archivo": nombre, "tabla": tabla, "escala": etiqueta,
                "filas": len(filas), "filas_base": base_n, "filas_sinteticas": len(filas) - base_n,
                "trabajadores_distintos": len({r["ID_Trabajador"] for r in filas}),
                "bytes": ruta.stat().st_size, "sha256": sha256(ruta),
                "TPA": ind["TPA"], "ICT": ind["ICT"], "TDT": ind["TDT"], "IEP": ind["IEP"],
                "validacion": "OK" if not errores else "; ".join(errores),
            })
        print(f"[OK]    Escala {etiqueta:>5}: {len(A)} asistencias, {len(T)} tareas | "
              f"TPA {ind['TPA']} %  ICT {ind['ICT']} %  TDT {ind['TDT']} %  IEP {ind['IEP']}")

    with open(salida / "manifiesto_datos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(manifiesto[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(manifiesto)
    meta = {
        "script": "generar_sinteticos.py", "version": VERSION,
        "fecha_generacion": datetime.now().isoformat(timespec="seconds"),
        "semilla": a.semilla, "escalas": escalas,
        "entradas": {"asistencia": str(a.asistencia), "tareas": str(a.tareas)},
        "regla": {
            "plantilla": "cada trabajador sintético copia fechas y tareas de un trabajador base elegido al azar",
            "primer_id_trabajador_sintetico": mapa[0][0] if mapa else None,
            "desfase_entrada_segundos": DESFASE_SEG,
            "limite_puntual": "antes de 09:41:00 = A tiempo; 09:41:00 o después = Tardanza",
            "hora_salida": "18:00:00",
            "fecha_calculada": modo_calc,
            "prob_variacion_tarea": PROB_VARIACION_TAREA,
            "estados_tarea": ESTADOS_TAREA, "marca_fuera_plazo": MARCA_FUERA_PLAZO,
        },
        "trabajadores_sinteticos_y_plantilla": [{"id": t, "plantilla": p} for t, p in mapa],
        "archivos": manifiesto,
    }
    (salida / "manifiesto_datos.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                                                  encoding="utf-8")
    print(f"[OK]    Archivos en: {salida.resolve()}")
    if hubo_error:
        sys.exit("[ERROR] Hubo errores de validación; revisar antes de subir a Databricks.")


if __name__ == "__main__":
    main()

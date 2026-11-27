#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruye el conjunto base (582 asistencias + 582 tareas) a partir de la lógica
de 01_Base_Datos/01_Estructura_y_Datos.sql, sin necesidad de SQL Server.

Se replica exactamente: trabajadores (1,2,3,5..11), jornadas L-V y L-M-V,
orden de inserción (IDs 1..582), estados de asistencia, estados de tareas,
observaciones, proyectos, Fecha, Fecha_Salida y Fecha_Entrega.

ÚNICA diferencia con la base de SQL Server: el script T-SQL usa
ABS(CHECKSUM(CONCAT(id,'-',yyyymmdd))) para variar los minutos de entrada dentro
de un rango. CHECKSUM es una función interna de SQL Server sin algoritmo publicado,
así que aquí se usa CRC32 del mismo texto. El minuto exacto puede cambiar, pero
siempre dentro del mismo rango, por lo que NO cambian los estados "A tiempo" /
"Tardanza", ni las tareas, ni los KPI (TPA, ICT, TDT, IEP).
Si se dispone de la exportación real de A&SG_OLTP, usar esa en lugar de este archivo.

Uso: python reconstruir_base_desde_repo.py --salida export_reconstruido
Genera Asistencia.csv y Tareas.csv (solo IDs; sin nombres, correos, teléfonos ni PIN).
"""
import argparse
import csv
import zlib
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

TRABAJADORES = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11]   # el 4 no existe en el padrón
TRES_DIAS = {2, 9, 11}                             # lunes, miércoles y viernes


def rnd(total, factor):
    """ROUND(total * factor, 0) de T-SQL (mitad hacia arriba, aritmética exacta)."""
    return int((Decimal(total) * Decimal(factor)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def variacion(id_trab, fecha):
    # Sustituto documentado de ABS(CHECKSUM(CONCAT(id, '-', yyyymmdd)))
    return zlib.crc32(f"{id_trab}-{fecha:%Y%m%d}".encode("utf-16-le")) & 0x7FFFFFFF


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--salida", default="export_reconstruido")
    a = p.parse_args()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)

    fechas = [date(2026, 7, 1) + timedelta(d) for d in range((date(2026, 9, 30) - date(2026, 7, 1)).days + 1)]
    # DATEDIFF(day,'19000101',fecha) % 7 : 0 = lunes
    dia = lambda f: (f - date(1900, 1, 1)).days % 7

    asistencias, tareas = [], []
    id_a = id_t = 1
    lim_correcciones = None
    for w in range(1, 12):
        jornadas = [f for f in fechas if w in TRABAJADORES and (
            (w not in TRES_DIAS and dia(f) <= 4) or (w in TRES_DIAS and dia(f) in (0, 2, 4)))]
        total = len(jornadas)
        for n, f in enumerate(jornadas, start=1):
            pos = ((n - 1) * 17 + w * 7) % total + 1
            v = variacion(w, f)
            if w == 2:
                minutos = 525 + v % 31 if pos <= rnd(total, "0.95") else 581 + v % 10
            elif w in (1, 3):
                minutos = 535 + v % 31 if pos <= rnd(total, "0.85") else 525 + v % 10
            elif w == 11:
                minutos = 570 if pos <= Decimal(total) * Decimal("0.50") else 585
            elif w == 9:
                minutos = 582 + v % 34 if pos <= rnd(total, "0.60") else 555 + v % 26
            else:
                minutos = 540 + v % 36 if pos <= rnd(total, "0.75") else 525 + v % 15
            medianoche = datetime(f.year, f.month, f.day)
            entrada = medianoche + timedelta(minutes=minutos)
            salida = medianoche + timedelta(hours=18)
            estado_a = "A tiempo" if minutos * 60 < 34860 else "Tardanza"
            asistencias.append([id_a, w, entrada, salida, f, estado_a])
            id_a += 1

            pos = ((n - 1) * 19 + w * 3) % total + 1
            proyecto = (n + w - 1) % 3 + 1
            obs = None
            if w == 2:
                lim_comp = rnd(total, "0.95")
                lim_prog = lim_comp + 1
            elif w == 9:
                lim_comp = rnd(total, "0.50")
                lim_prog = rnd(total, "0.80")
                if pos <= lim_comp:
                    obs = "[ENTREGADO FUERA DE PLAZO]"
            else:
                fc = {1: "0.90", 3: "0.80", 11: "0.40"}.get(w, "0.65")
                fp = {1: "0.95", 3: "0.90", 11: "0.70"}.get(w, "0.85")
                lim_comp, lim_prog = rnd(total, fc), rnd(total, fp)
                lim_correcciones = rnd(total, "0.10")
                if pos <= lim_correcciones:
                    obs = "Corregir las medidas y adjuntar el sustento actualizado."
            estado_t = "Completada" if pos <= lim_comp else ("En Progreso" if pos <= lim_prog else "Asignada")
            inicio = None if estado_t == "Asignada" else entrada + timedelta(minutes=15)
            if estado_t != "Completada":
                entrega = None
            elif obs == "[ENTREGADO FUERA DE PLAZO]":
                entrega = medianoche + timedelta(days=1, hours=10)
            else:
                entrega = medianoche + timedelta(hours=17)
            tareas.append([id_t, w, proyecto, f, inicio, entrega, estado_t, obs])
            id_t += 1

    fmt = lambda x: "" if x is None else (x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, datetime)
                                          else x.isoformat() if isinstance(x, date) else x)
    with open(out / "Asistencia.csv", "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["ID_Asistencia", "ID_Trabajador", "Fecha_Entrada", "Fecha_Salida", "Fecha_Calculada", "Estado_Asistencia"])
        wr.writerows([[fmt(x) for x in r] for r in asistencias])
    with open(out / "Tareas.csv", "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["ID_Tarea", "ID_Trabajador", "ID_Proyecto", "Fecha", "Fecha_Inicio", "Fecha_Entrega", "Estado_Tarea", "Observaciones"])
        wr.writerows([[fmt(x) for x in r] for r in tareas])

    # Controles contra las evidencias del repositorio
    meses = {}
    for r in asistencias:
        m = meses.setdefault(r[4].month, [0, 0])
        m[0] += 1
        m[1] += r[5] == "Tardanza"
    print("Mes | asistencias | tardanzas  (esperado: 7=203/15, 8=186/15, 9=193/16)")
    for k in sorted(meses):
        print(f"  {k} | {meses[k][0]} | {meses[k][1]}")
    print("Por trabajador: asist | TPA | ICT | TDT | IEP")
    for w in TRABAJADORES:
        A = [r for r in asistencias if r[1] == w]
        T = [r for r in tareas if r[1] == w]
        tpa = 100 * sum(r[5] == "A tiempo" for r in A) / len(A)
        ict = 100 * sum(r[6] == "Completada" and r[7] is None for r in T) / len(T)
        tdt = 100 * sum(r[7] is not None and "FUERA DE PLAZO" in r[7] for r in T) / len(T)
        print(f"  {w:>2} | {len(A)} | {tpa:6.2f} | {ict:6.2f} | {tdt:6.2f} | {0.3*tpa+0.5*ict+0.2*(100-tdt):6.2f}")
    print(f"Total: {len(asistencias)} asistencias, {len(tareas)} tareas -> {out.resolve()}")


if __name__ == "__main__":
    main()

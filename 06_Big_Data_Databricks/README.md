# 06 · Big Data — Databricks + Apache Spark (EXP-02)

Evaluación de la carga y la consulta del conjunto de asistencias y tareas a tres escalas: 582, 5 000 y 10 000 filas por tabla.
Evidencias **E-08** y **E-14** del informe (puntos 4.2, 4.5, 5.3, 6.2–6.5 y 7.1).

## Contenido

| Carpeta | Archivo | Uso |
|---|---|---|
| `scripts/` | `exportar_base.sql` | Consultas para exportar `Asistencia` y `Tareas` de A&SG_OLTP desde SSMS (solo IDs). |
| `scripts/` | `reconstruir_base_desde_repo.py` | Reconstruye las 582 + 582 filas a partir de la lógica de `01_Base_Datos/01_Estructura_y_Datos.sql`, sin SQL Server. |
| `scripts/` | `generar_sinteticos.py` | Valida la base y genera las escalas 5 000 y 10 000 (semilla 2026), con manifiesto. |
| `datos/` | `asistencias_*.csv`, `tareas_*.csv` | Conjunto base y escalas sintéticas usados en Databricks. |
| `datos/` | `manifiesto_datos.csv` / `.json` | Filas, bytes, SHA-256, semilla, regla de generación y KPI por archivo. |
| `notebook/` | `EXP02_Databricks_Rendimiento.ipynb` | Pasos 4–20 de la guía: esquema, volumen, tablas, consultas, mediciones y gráfico. |
| `resultados/` | CSV de tiempos, resumen, registro RUN, KPI por escala y gráfico | Salidas de la ejecución en Databricks. |
| `capturas/` | `D-01` … `D-09` | Capturas con fecha y código de celda visibles. |

## Cómo reproducir

```bash
cd 06_Big_Data_Databricks/scripts
python reconstruir_base_desde_repo.py --salida export        # o exportar con exportar_base.sql
python generar_sinteticos.py --asistencia export/Asistencia.csv --tareas export/Tareas.csv --salida ../datos
```

Luego importar `notebook/EXP02_Databricks_Rendimiento.ipynb` en Databricks y ejecutarlo de arriba hacia abajo.

## Origen de los datos

- **Base (582 + 582):** se reconstruyó con `reconstruir_base_desde_repo.py`, que replica el generador T-SQL del repositorio. Coincide con
  las evidencias existentes: 203/186/193 asistencias por mes, 15/15/16 tardanzas, los KPI por trabajador de
  `04_Documentacion/Evidencias/03_Resultados_Padron_Origen.txt` y los globales **TPA 92,10 %, ICT 56,36 %, TDT 3,44 %, IEP 75,12**.
  La única diferencia es el minuto exacto de entrada: el T-SQL lo varía con `CHECKSUM` (función interna de SQL Server) y el script usa CRC32.
  El minuto cambia dentro del mismo rango, así que no cambian los estados ni los KPI.
- **Escalas sintéticas:** cada trabajador sintético (ID desde 1001) copia las fechas y tareas de un trabajador base elegido con la semilla;
  la hora de entrada varía ±5 min. Se mantienen la regla de 09:41:00, la salida a las 18:00, una fila por trabajador y día, y los estados
  Completada / En Progreso / Asignada. La escala de 10 000 contiene a la de 5 000. No hay nombres, correos, teléfonos ni PIN.
- Los scripts y el notebook se elaboraron con ayuda de IA (Claude), con verificación del grupo (ver 5.7 del informe).

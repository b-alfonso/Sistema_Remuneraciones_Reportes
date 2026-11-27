# 06 · Big Data — Databricks + Apache Spark (EXP-02)

Evaluación de la carga y la consulta del conjunto de asistencias y tareas a tres escalas: 582, 5 000 y 10 000 filas por tabla.
Evidencias **E-08** y **E-14** del informe (puntos 4.2, 4.5, 5.3, 6.2–6.5 y 7.1).

## Solución Big Data completa (Medallion)

La carpeta [`solucion_medallion/`](solucion_medallion) contiene la solución pedida en la entrega final: EDA, limpieza, capas
Bronze/Silver/Gold, KPI, visualizaciones y dashboard de Databricks, con su diagrama de arquitectura y guía de replicación.

**¿Nunca usaste Databricks?** Empieza por la [guía rápida](GUIA_RAPIDA_DATABRICKS.md).

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

## Resultados de la ejecución (21/11/2026, Databricks Free Edition, serverless)

Entorno (captura D-09): Spark 4.2.0, runtime `client.6.6` (variable `DATABRICKS_RUNTIME_VERSION`), Python 3.12.3, compute serverless.
Método: por escala y operación, 1 calentamiento (no entra en el resumen) + 5 repeticiones medidas con `time.perf_counter`.
Carga = leer el CSV del volumen + `saveAsTable` (overwrite). Consulta = `COUNT(*) … GROUP BY` + `collect()`.

| Escala | Operación | Mediana (s) | Mín. (s) | Máx. (s) |
|---:|---|---:|---:|---:|
| 582 | carga asistencias | 2,2914 | 1,9490 | 2,4674 |
| 582 | carga tareas | 1,9786 | 1,9591 | 2,0347 |
| 582 | consulta asistencias | 0,6419 | 0,6342 | 0,7030 |
| 582 | consulta tareas | 0,6124 | 0,5985 | 0,6598 |
| 5 000 | carga asistencias | 1,8955 | 1,8466 | 1,9905 |
| 5 000 | carga tareas | 1,8502 | 1,7227 | 1,8953 |
| 5 000 | consulta asistencias | 0,6640 | 0,5523 | 0,7596 |
| 5 000 | consulta tareas | 0,5706 | 0,5450 | 0,5959 |
| 10 000 | carga asistencias | 1,7807 | 1,7494 | 1,8952 |
| 10 000 | carga tareas | 1,7938 | 1,7505 | 1,8287 |
| 10 000 | consulta asistencias | 0,5493 | 0,5199 | 0,6180 |
| 10 000 | consulta tareas | 0,5727 | 0,5312 | 0,6118 |

KPI calculados en Databricks (`resultados/kpi_por_escala.csv`): la escala base da **TPA 92,10 %, ICT 56,36 %, TDT 3,44 %, IEP 75,12**,
igual que Power BI. Las escalas 5 000 y 10 000 coinciden con el manifiesto del generador.

Capturas: `D-01` … `D-09` (pasos 4–14), `T-01` (CSV de tiempos y resumen), `T-02` (registro RUN-03 a RUN-05 y KPI por escala),
`T-03` (gráfico tiempo vs. filas). Los códigos E-xx los asigna el encargado.

# Solución Big Data en Databricks · Arquitectura Medallion

Notebook [`BigData_Solucion_Medallion.ipynb`](BigData_Solucion_Medallion.ipynb): ingesta, EDA, limpieza, capas Bronze/Silver/Gold,
indicadores, visualizaciones y dashboard de Databricks sobre los datos de asistencias y tareas (BASAV · Grupo 2).
Responsable: Luis Obregón Hidalgo. Ejecutado el 26/11/2026 en Databricks Free Edition (serverless).

- Arquitectura: [`arquitectura_solucion_databricks.png`](arquitectura_solucion_databricks.png)
- Cómo replicarlo: [`GUIA_REPLICACION.md`](GUIA_REPLICACION.md)
- Evidencias: [`capturas/`](capturas) (S-01 … S-12)

## Capas y tablas (Unity Catalog, formato Delta)

| Capa | Tablas | Filas |
|---|---|---|
| `mon_bronze` | `asistencias`, `tareas` (texto crudo + `_escala`, `_archivo_origen`, `_fecha_ingesta`) | 15 582 cada una |
| `mon_silver` | `asistencias`, `tareas` (limpias y tipadas), `tareas_cuarentena`, `diagnostico_calidad` | 15 582 · 15 582 · 527 · 45 |
| `mon_gold` | `kpi_global`, `kpi_mes`, `kpi_trabajador`, `kpi_trabajador_mes` | 3 · 9 · 267 · 800 |

15 582 = 582 (datos del Data Mart) + 5 000 + 10 000 (sintéticos, semilla 2026).

## Operaciones PySpark usadas

`read.csv`, `printSchema`, `describe`, `summary`, `groupBy`/`agg`, `filter`, `select`, `withColumnRenamed`, `withColumn`,
`cast`/`try_cast`, `trim`, `na.drop`, `na.fill`, `dropDuplicates`, `when`, `join`, `Window`/`rank`, `unionByName`,
`saveAsTable` (Delta), `COMMENT ON TABLE`, `DESCRIBE HISTORY`.

## Resultados principales

| Comprobación | Resultado | Captura |
|---|---|---|
| Nulos en la base (582 filas) | 0 en claves y fechas de asistencias; tareas: `Fecha_Inicio` 81 (13,92 %), `Fecha_Entrega` 181 (31,10 %), `Observaciones` 509 (87,46 %) — vacíos esperados según el estado | S-03b |
| Reglas de calidad en Bronze | 0 incumplimientos en la base; "Completada sin fecha de entrega": 142 (5 000) y 300 (10 000); "En Progreso sin fecha de inicio": 30 y 55 | S-05 |
| Conciliación Bronze → Silver | 0 filas descartadas en las tres escalas; 527 tareas marcadas en cuarentena (no se borran) | S-07 |
| KPI Gold escala base vs Power BI | TPA 92,10 · ICT 56,36 · TDT 3,44 · IEP 75,12 — **coinciden** (diferencia 0) | S-09 |
| KPI por mes (base) | jul 92,61 / 57,14 / 3,45 / 75,67 · ago 91,94 / 57,53 / 3,76 / 75,59 · sep 91,71 / 54,40 / 3,11 / 74,09 (TPA/ICT/TDT/IEP) | S-08 |
| IEP por trabajador (base) | máximo 96,00 (ID 2), mínimo 22,00 (ID 9) | S-09 |
| Dashboard | "BASAV · Monitoreo de empleados (Gold)", publicado: 6 tarjetas, KPI por mes, IEP por trabajador, KPI por escala, cuarentena | S-12a |

Los KPI de las escalas 5 000 y 10 000 son sintéticos: sirven para probar el pipeline con más volumen, no describen a trabajadores reales.

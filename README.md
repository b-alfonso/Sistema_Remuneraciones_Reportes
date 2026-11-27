# Sistema automatizado para el monitoreo de empleados · BASAV Grupo 2

Proyecto final del curso **Base de Datos Avanzadas y Big Data** (UPN, 2026-2). El sistema registra asistencias y tareas de los
trabajadores, las integra en un Data Mart y calcula cuatro indicadores de rendimiento:

| Indicador | Fórmula |
|---|---|
| **TPA** · tasa de puntualidad | asistencias "A tiempo" / asistencias × 100 (entrada antes de las 09:41) |
| **ICT** · índice de cumplimiento de tareas | tareas Completadas sin observación / tareas × 100 |
| **TDT** · tasa de tareas fuera de plazo | tareas con "FUERA DE PLAZO" en observaciones / tareas × 100 |
| **IEP** · índice de eficiencia del personal | 0,3·TPA + 0,5·ICT + 0,2·(100 − TDT) |

Conjunto inicial: 10 trabajadores, 582 asistencias y 582 tareas de julio a septiembre de 2026 (datos simulados).
Resultado global esperado: **TPA 92,10 % · ICT 56,36 % · TDT 3,44 % · IEP 75,12**, igual en Power BI y en Databricks.

## Arquitectura

```
SQL Server (A&SG_OLTP) ──ETL──► A&SG_DataMart (modelo estrella) ──► Power BI (dashboards)       ← solución BI
        │
        └─ exportación CSV (solo IDs) ──► Databricks: volumen ► Bronze ► Silver ► Gold ► dashboard ← solución Big Data
```

## Contenido del repositorio

| Carpeta | Qué contiene |
|---|---|
| [`01_Base_Datos`](01_Base_Datos) | Creación y llenado de `A&SG_OLTP`, creación del Data Mart, carga y comprobación de la simulación. |
| [`02_Procedimientos_Almacenados`](02_Procedimientos_Almacenados) | Procedimiento ETL `usp_cargar_rendimiento` y vistas para Power BI. |
| [`03_Vistas_PowerBI`](03_Vistas_PowerBI) | Reportes `.pbix` y capturas de los dashboards. |
| [`04_Documentacion`](04_Documentacion) | Modelo y reglas, indicadores, validación del ETL, registro de cambios y evidencias. |
| [`05_Procedimientos_Replicacion`](05_Procedimientos_Replicacion) | Guía completa para replicar la solución BI paso a paso. |
| [`06_Big_Data_Databricks`](06_Big_Data_Databricks) | Solución Big Data en Databricks (Medallion, EDA, limpieza, KPI, dashboard) y experimento de escalado EXP-02. |

## Cómo replicar

**Solución BI (SQL Server + Power BI).** Seguir [`04_Documentacion/00_Orden_Ejecucion.md`](04_Documentacion/00_Orden_Ejecucion.md)
y luego la [guía completa](05_Procedimientos_Replicacion/09_Guia_Completa.md).

**Solución Big Data y experimentos (Databricks).** Para quien nunca usó Databricks: [guía rápida](06_Big_Data_Databricks/GUIA_RAPIDA_DATABRICKS.md). Detalle técnico:
[`06_Big_Data_Databricks/solucion_medallion/GUIA_REPLICACION.md`](06_Big_Data_Databricks/solucion_medallion/GUIA_REPLICACION.md).
Requiere una cuenta de Databricks Free Edition; no necesita SQL Server porque los CSV ya están en `06_Big_Data_Databricks/exp02-Escalabilidad/archivos-csv`.

## Herramientas

SQL Server y SSMS · Power BI Desktop · Databricks Free Edition (Apache Spark, Delta Lake, Unity Catalog, dashboards AI/BI) ·
Python 3 · GitHub.

## Privacidad y uso de IA

Los datos son simulados. Las exportaciones hacia Databricks usan solo identificadores de trabajador (sin nombres, correos,
teléfonos ni PIN). El uso de herramientas de inteligencia artificial está declarado en el punto 5.7 del informe final.

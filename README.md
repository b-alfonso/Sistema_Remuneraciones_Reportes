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
                                                   │
                                                   └─► Experimentos EXP-02 y EXP-04 a EXP-07 (tiempos medidos en Spark)
```

## Contenido del repositorio

| Carpeta | Qué contiene |
|---|---|
| [`01_Base_Datos`](01_Base_Datos) | Creación y llenado de `A&SG_OLTP`, creación del Data Mart, carga y comprobación de la simulación. |
| [`02_Procedimientos_Almacenados`](02_Procedimientos_Almacenados) | Procedimiento ETL `usp_cargar_rendimiento` y vistas para Power BI. |
| [`03_Vistas_PowerBI`](03_Vistas_PowerBI) | Reportes `.pbix` y capturas de los dashboards. |
| [`04_Documentacion`](04_Documentacion) | Modelo y reglas, indicadores, validación del ETL, registro de cambios y evidencias. |
| [`05_Procedimientos_Replicacion`](05_Procedimientos_Replicacion) | Guía completa para replicar la solución BI paso a paso. |
| [`06_Big_Data_Databricks`](06_Big_Data_Databricks) | Solución Big Data en Databricks: arquitectura Medallion, dashboard y experimentos EXP-02 y EXP-04 a EXP-07 (detalle abajo). |

### Solución Big Data y experimentos (`06_Big_Data_Databricks`)

| Carpeta | Contenido | Evidencia | Responsable |
|---|---|---|---|
| [`solucion_medallion`](06_Big_Data_Databricks/solucion_medallion) | Notebook `BigData_Solucion_Medallion`: capas Bronze, Silver y Gold en Delta (Unity Catalog), diagnóstico de calidad, KPI iguales a Power BI, dashboard AI/BI, arquitectura y guía de replicación. | E-18 | Luis Obregón |
| [`exp02-Escalabilidad`](06_Big_Data_Databricks/exp02-Escalabilidad) | **EXP-02.** Carga y consulta con 582, 5 000 y 10 000 filas por tabla. Notebook `EXP02_Databricks_Rendimiento`, CSV de datos y de mediciones. | E-08 | Luis Obregón |
| [`exp04-Ingesta`](06_Big_Data_Databricks/exp04-Ingesta) | **EXP-04.** Lectura con esquema explícito (`StructType`) frente a `inferSchema`. Notebook `exp_04_Ingesta`. | E-19 | Victor Paredes |
| [`exp05-Formatos`](06_Big_Data_Databricks/exp05-Formatos) | **EXP-05.** Tamaño y latencia de consulta en CSV, Parquet y Delta. Notebook `EXP05_FORMATOS`. | E-20 | Fernando Carhuatanta |
| [`exp06-Particion`](06_Big_Data_Databricks/exp06-Particion) | **EXP-06.** Tabla Delta sin partición, particionada por mes y por estado. Notebook `EXP06_Particionamiento`. | E-21 | Benjamin Alfonso |
| [`exp07-Analitica`](06_Big_Data_Databricks/exp07-Analitica) | **EXP-07.** Cálculo del IEP por trabajador con DataFrame API, Spark SQL y `cache()`. Notebook `EXP07_Analitica`. | E-22 | Diego Garrido |

Cada carpeta de experimento incluye el notebook exportado (HTML), el CSV con la tabla de resultados y las capturas.

### Experimentos EXP-04 a EXP-07

Los cuatro experimentos usan el mismo par de archivos, `asistencias_15000.csv` y `tareas_15000.csv` (15 000 filas cada uno, 262 trabajadores),
generados con `generar_15000.py` (semilla 2026). Cada uno corre en su propio notebook y esquema de Unity Catalog, con compute serverless de
Databricks Free Edition.

**Medición.** Un calentamiento (no se cuenta) y cinco repeticiones, una a la vez, con `time.perf_counter`; se reportan mediana, mínimo y máximo.
Antes de reportar tiempos se valida que todas las variantes devuelvan el mismo resultado.

| Experimento | Qué compara | Resultado principal (mediana) |
|---|---|---|
| EXP-04 Ingesta | Esquema explícito frente a `inferSchema` | Lectura de asistencias: 0,634 s frente a 1,081 s; de tareas: 0,590 s frente a 1,094 s. Los tipos de dato resultaron iguales. |
| EXP-05 Formatos | CSV, Parquet y Delta | Consulta: CSV 1,403 s, Parquet 0,974 s, Delta 0,506 s. Parquet fue el más pequeño (185 465 bytes frente a 1 211 150 del CSV). |
| EXP-06 Partición | Sin partición, por mes y por estado | 0,7294 s, 0,6769 s y 0,6711 s, con rangos superpuestos: sin ventaja distinguible con 15 000 filas. |
| EXP-07 Analítica | DataFrame API, Spark SQL y `cache()` | 0,680 s, 0,749 s y 1,107 s. Mismo ranking y mismos KPI en las tres variantes. |

Limitaciones: 15 000 filas, datos sintéticos, una sola sesión y compute serverless sin acceso a CPU, RAM ni Spark UI.

## Cómo replicar

**Solución BI (SQL Server + Power BI).** Seguir [`04_Documentacion/00_Orden_Ejecucion.md`](04_Documentacion/00_Orden_Ejecucion.md)
y luego la [guía completa](05_Procedimientos_Replicacion/09_Guia_Completa.md).

**Solución Big Data y experimentos (Databricks).** Para quien nunca usó Databricks: [guía rápida](06_Big_Data_Databricks/GUIA_RAPIDA_DATABRICKS.md). Detalle técnico:
[`06_Big_Data_Databricks/solucion_medallion/GUIA_REPLICACION.md`](06_Big_Data_Databricks/solucion_medallion/GUIA_REPLICACION.md).
Requiere una cuenta de Databricks Free Edition; no necesita SQL Server porque los CSV ya están en el repositorio.

1. Crear una cuenta en Databricks Free Edition.
2. En el catálogo `workspace`, crear el esquema, el volumen y el directorio que indica cada guía.
3. Subir al volumen los CSV de la carpeta del experimento: [`exp02-Escalabilidad/archivos-csv`](06_Big_Data_Databricks/exp02-Escalabilidad/archivos-csv) para EXP-02 y los de cada carpeta `exp04` a `exp07` para los demás.
4. Importar el notebook de la carpeta y ejecutarlo con **Run all** en compute serverless.
5. Comparar los resultados con las tablas del informe (sección 5.3 y capítulo VI).

> En serverless, el DBFS raíz público está deshabilitado: las rutas deben ser de volumen, con la forma `/Volumes/workspace/<esquema>/<volumen>/<directorio>/`.

## Herramientas

SQL Server y SSMS · Power BI Desktop · Databricks Free Edition (Apache Spark, Delta Lake, Parquet, Unity Catalog, dashboards AI/BI, Genie) ·
Python 3 · GitHub.

## Privacidad y uso de IA

Los datos son simulados. Las exportaciones hacia Databricks usan solo identificadores de trabajador (sin nombres, correos,
teléfonos ni PIN). El uso de herramientas de inteligencia artificial (Gemini, Claude y Genie de Databricks) está declarado en el punto 5.7 del informe final.

## Equipo

Alfonso Sanchez B. · Carhuatanta Cabrera F. · Garrido Asencio D. · Obregon Hidalgo L. · Paredes Ramos V.

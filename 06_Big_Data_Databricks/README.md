# 06 · Big Data — Databricks + Apache Spark

Solución Big Data del proyecto BASAV (Grupo 2) y experimentaciones de rendimiento en Databricks Free Edition.
Cada experimentación tiene su propia carpeta con `README.md` (resumen y resultados), `GUIA_EJECUCION_EXPERIMENTACION.md`
(paso a paso para quien nunca usó Databricks), `archivos-csv/` y `capturas/`.

**¿Nunca usaste Databricks?** Empieza por la [guía rápida](GUIA_RAPIDA_DATABRICKS.md).

## Solución Big Data (arquitectura Medallion)

| Carpeta | Contenido |
|---|---|
| [`solucion_medallion/`](solucion_medallion) | EDA, limpieza, capas Bronze/Silver/Gold, KPI, visualizaciones y dashboard de Databricks, con diagrama de arquitectura y guía de replicación. KPI Gold iguales a Power BI. |

## Experimentaciones

| Carpeta | Experimento | Responsable | Resumen |
|---|---|---|---|
| [`exp02-Escalabilidad/`](exp02-Escalabilidad) | **EXP-02: Escalabilidad por volumen de datos** | Luis Obregón | Mide el tiempo de carga (CSV → Delta) y de consulta (`GROUP BY`) con 582, 5 000 y 10 000 filas por tabla, 5 repeticiones cada uno (72 mediciones). Los tiempos no aumentan con el volumen y los KPI de la base son iguales a Power BI. |
| [`exp04-Ingesta/`](exp04-Ingesta) | **EXP-04: Ingesta (Esquema Explícito vs `inferSchema`)** | | Evalúa el impacto en tiempo de lectura y tipado de datos al cargar 15 000 filas de asistencias y tareas con esquema definido (`StructType`) frente a inferencia automática (`inferSchema`). |
| [`exp05-Formatos/`](exp05-Formatos) | **EXP-05: Formatos de Almacenamiento (CSV vs Parquet vs Delta)** | | Compara el tamaño en disco (compresión Snappy), tiempo de persistencia y latencia de consultas agregadas (`GROUP BY`) entre CSV plano, Parquet columnar y tablas Delta Lake. |
| [`exp06-Particion/`](exp06-Particion) | **EXP-06: Particionamiento de Tablas Delta** | | Analiza la optimización por poda de particiones (*partition pruning*) al particionar por mes vs estado frente a una tabla sin particionar, evaluando la prevención del problema de archivos pequeños. |
| [`exp07-Analitica/`](exp07-Analitica) | **EXP-07: Consulta Analítica con Join y KPIs (IEP)** | | Mide la latencia al calcular indicadores de desempeño (TPA, ICT, TDT, IEP) uniendo asistencias y tareas para 262 trabajadores, comparando DataFrame API, Spark SQL y el impacto de `cache()`. |

## Orden recomendado para replicar

1. **EXP-02** primero: crea el esquema `bd_rendimiento` y el volumen con los CSV que usa la solución Medallion.
2. **Solución Medallion** (`solucion_medallion/`).
3. EXP-04 a EXP-07, cada uno con sus propios CSV de 15 000 filas.

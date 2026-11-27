# Guía de Ejecución de la Experimentación: EXP-04 Ingesta de Datos

## 1. Identificación y Objetivos
- **Código de Experimento:** `EXP-04`
- **Nombre:** Ingesta de Datos y Validación de Esquemas en Databricks / Apache Spark.
- **Módulo:** `06_Big_Data_Databricks/exp04-Ingesta`
- **Objetivo Principal:** Evaluar y estandarizar el proceso de ingestión de datos crudos (archivos CSV de `Asistencia` y `Tareas`) hacia el entorno de Databricks, aplicando validación estricta de esquemas (`StructType`), manejo de registros corruptos y medición de tiempos de carga en las 3 escalas del proyecto (582, 5 000 y 10 000 filas).

---

## 2. Estructura del Directorio
```
exp04-Ingesta/
├── README.md                           <- Esta guía de ejecución
├── GUIA_EJECUCION_EXPERIMENTACION.md   <- Copia de la guía de ejecución
├── capturas/                           <- Evidencias fotográficas (código, celdas y esquemas)
└── archivos-csv/                       <- Métricas de ingesta y resultados exportados
```

---

## 3. Requisitos Previos y Entorno
1. **Datos de Entrada:**
   - Archivos fuente ubicados en `06_Big_Data_Databricks/datos/`:
     - `asistencias_base_582.csv` / `tareas_base_582.csv`
     - `asistencias_sinteticas_5000.csv` / `tareas_sinteticas_5000.csv`
     - `asistencias_sinteticas_10000.csv` / `tareas_sinteticas_10000.csv`
2. **Entorno de Ejecución:**
   - Databricks Runtime (DBR) 13.x+ / Databricks Serverless Compute.
   - Python 3.10+ / PySpark 3.4+.

---

## 4. Procedimiento de Ejecución Paso a Paso

### Paso 1: Carga de Archivos a Databricks (Volumes / DBFS)
Subir los archivos CSV fuente al volumen de Unity Catalog o DBFS:
```python
# Definición de rutas base
RUTA_VOLUMEN = "/Volumes/workspace/default/datos_remuneraciones"
# o ruta DBFS: "dbfs:/FileStore/remuneraciones/datos"
```

### Paso 2: Definición Explícita de Esquemas (`StructType`)
Para evitar la sobrecarga del análisis predictivo de tipos (`inferSchema=True`), definir los esquemas fuertemente tipados:
```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DecimalType

schema_asistencia = StructType([
    StructField("id_asistencia", IntegerType(), False),
    StructField("id_trabajador", IntegerType(), False),
    StructField("fecha", DateType(), False),
    StructField("hora_entrada", StringType(), True),
    StructField("hora_salida", StringType(), True),
    StructField("estado_asistencia", StringType(), False)
])

schema_tareas = StructType([
    StructField("id_tarea", IntegerType(), False),
    StructField("id_trabajador", IntegerType(), False),
    StructField("fecha", DateType(), False),
    StructField("horas_trabajadas", DecimalType(5, 2), False),
    StructField("estado_tarea", StringType(), False),
    StructField("tipo_tarea", StringType(), True)
])
```

### Paso 3: Ejecución de Ingesta y Validación de Errores
Cargar los datos utilizando el modo permisivo o de captura de corrupción:
```python
import time

def ingestar_csv(ruta_csv, schema):
    t_inicio = time.perf_counter()
    df = (spark.read
          .format("csv")
          .option("header", "true")
          .option("mode", "DROPMALFORMED")
          .schema(schema)
          .load(ruta_csv))
    conteo = df.count()
    t_fin = time.perf_counter()
    duracion = t_fin - t_inicio
    return df, conteo, duracion
```

### Paso 4: Registro de Métricas y Tiempos
Ejecutar la ingesta para las 3 escalas y registrar los resultados en `archivos-csv/metricas_ingesta.csv`:
- Escala 1 (582 filas)
- Escala 2 (5 000 filas)
- Escala 3 (10 000 filas)

---

## 5. Entregables y Evidencias
- [ ] Guardar las capturas de pantalla de la ingesta en `capturas/` con nomenclatura `CAP-EXP04-01_Schema.png`, `CAP-EXP04-02_Tiempos_Ingesta.png`.
- [ ] Exportar la tabla resumen de tiempos en `archivos-csv/metricas_ingesta.csv`.

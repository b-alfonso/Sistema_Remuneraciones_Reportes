# Guía de Ejecución de la Experimentación: EXP-06 Particionamiento de Datos

## 1. Identificación y Objetivos
- **Código de Experimento:** `EXP-06`
- **Nombre:** Estrategias de Particionamiento y Optimización de Consultas en Databricks.
- **Módulo:** `06_Big_Data_Databricks/exp06-Particion`
- **Objetivo Principal:** Analizar el impacto de la partición física de datos (`partitionBy`) frente a datos no particionados en el almacenamiento de tablas de asistencias y tareas, evaluando el beneficio del *Partition Pruning* (poda de particiones) y previniendo el problema de archivos pequeños (*Small Files Problem*).

---

## 2. Estructura del Directorio
```
exp06-Particion/
├── README.md                           <- Esta guía de ejecución
├── GUIA_EJECUCION_EXPERIMENTACION.md   <- Copia de la guía de ejecución
├── capturas/                           <- Evidencias de planes de ejecución y particiones
└── archivos-csv/                       <- CSVs con mediciones y tiempos de respuesta
```

---

## 3. Criterios de Particionamiento
1. **Columna Candidata Temporal (`anio_mes`):**
   - Ideal para consultas de rango mensual utilizadas en el cálculo de planillas y remuneraciones.
2. **Columna de Estado (`estado_asistencia`):**
   - Evaluar si la baja cardinalidad justifica o no una subpartición.
3. **Evitar Sobrealmacenamiento:**
   - No particionar por `id_trabajador` debido a la dispersión en micro-archivos cuando las filas por trabajador son inferiores a ~1 000.

---

## 4. Procedimiento de Ejecución Paso a Paso

### Paso 1: Preparación de Datos y Derivación de Columnas Clave
Agregar la columna de partición temporal en el DataFrame:
```python
from pyspark.sql.functions import col, date_format

df_enriquecido = df_asistencias.withColumn("anio_mes", date_format(col("fecha"), "yyyy-MM"))
```

### Paso 2: Creación de Versión No Particionada vs Particionada
```python
# Versión 1: Tabla No Particionada
df_enriquecido.write.format("delta").mode("overwrite").save("/tmp/exp06/no_particionado")

# Versión 2: Tabla Particionada por anio_mes
df_enriquecido.write.format("delta").partitionBy("anio_mes").mode("overwrite").save("/tmp/exp06/particionado")
```

### Paso 3: Inspección de Estructura de Directorios
Verificar la estructura de subcarpetas generadas en el sistema de archivos:
```python
display(dbutils.fs.ls("/tmp/exp06/particionado"))
```
Deberán observarse directorios como `anio_mes=2026-08/`, `anio_mes=2026-09/`, etc.

### Paso 4: Evaluación de Rendimiento y Plan de Ejecución (`EXPLAIN`)
Comparar los tiempos de ejecución y analizar el plan físico:
```python
import time

query_filtro = "anio_mes = '2026-09'"

# Consulta en tabla No Particionada
t0 = time.perf_counter()
res_no_part = spark.read.format("delta").load("/tmp/exp06/no_particionado").filter(query_filtro).count()
t_no_part = time.perf_counter() - t0

# Consulta en tabla Particionada (Aplica Partition Pruning)
t0 = time.perf_counter()
res_part = spark.read.format("delta").load("/tmp/exp06/particionado").filter(query_filtro).count()
t_part = time.perf_counter() - t0

# Ver plan de ejecución para confirmar PartitionFilters
spark.read.format("delta").load("/tmp/exp06/particionado").filter(query_filtro).explain()
```

---

## 5. Entregables y Evidencias
- [ ] Captura del plan de ejecución (`EXPLAIN`) mostrando `PartitionFilters: [isnotnull(anio_mes#...)]` en `capturas/`.
- [ ] Captura del árbol de directorios de particiones en `capturas/`.
- [ ] Exportación de métricas a `archivos-csv/metricas_particionamiento.csv`.

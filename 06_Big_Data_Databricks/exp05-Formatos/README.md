# Guía de Ejecución de la Experimentación: EXP-05 Formatos de Almacenamiento

## 1. Identificación y Objetivos
- **Código de Experimento:** `EXP-05`
- **Nombre:** Comparativa de Rendimiento y Compresión en Formatos de Almacenamiento (CSV vs Parquet vs Delta Lake).
- **Módulo:** `06_Big_Data_Databricks/exp05-Formatos`
- **Objetivo Principal:** Evaluar el impacto en espacio de almacenamiento en disco, velocidad de escritura (write latency) y velocidad de lectura (read latency) al persistir los datos de asistencias y tareas en tres formatos distintos: CSV tradicional, Apache Parquet (columnar comprimido con Snappy) y tablas Delta Lake.

---

## 2. Estructura del Directorio
```
exp05-Formatos/
├── README.md                           <- Esta guía de ejecución
├── GUIA_EJECUCION_EXPERIMENTACION.md   <- Copia de la guía de ejecución
├── capturas/                           <- Evidencias de ejecuciones, tamaños y tiempos
└── archivos-csv/                       <- CSVs con métricas de compresión y benchmarks
```

---

## 3. Matriz de Comparación Técnica

| Característica | Formato CSV | Apache Parquet | Delta Lake |
|---|---|---|---|
| **Estructura** | Fila (texto plano) | Columnar binario | Columnar (Parquet + Transaction Log) |
| **Compresión** | Sin compresión / GZIP | Snappy (por defecto) | Snappy + ZSTD |
| **Soporte ACID** | No | No | Sí (ACID Transactions) |
| **Time Travel** | No | No | Sí (`VERSION AS OF`) |
| **Optimización** | Ninguna | Pushdown de predicados | Compaction, Z-Ordering, Data Skipping |

---

## 4. Procedimiento de Ejecución Paso a Paso

### Paso 1: Carga del DataFrame Base
Cargar el conjunto de datos estandarizado (escala 10 000 para evidenciar diferencias significativas).
```python
df_asistencias = spark.table("bronze_asistencias")
```

### Paso 2: Benchmark de Escritura y Tamaño en Disco
Persistir el mismo DataFrame en las tres tecnologías midiendo tiempo de escritura:
```python
import time

# 1. Escritura en CSV
t0 = time.perf_counter()
df_asistencias.write.mode("overwrite").option("header", "true").csv("/tmp/exp05/csv")
t_csv_w = time.perf_counter() - t0

# 2. Escritura en Parquet
t0 = time.perf_counter()
df_asistencias.write.mode("overwrite").parquet("/tmp/exp05/parquet")
t_parquet_w = time.perf_counter() - t0

# 3. Escritura en Delta Lake
t0 = time.perf_counter()
df_asistencias.write.format("delta").mode("overwrite").save("/tmp/exp05/delta")
t_delta_w = time.perf_counter() - t0
```

### Paso 3: Benchmark de Lectura y Filtrado por Predicado
Medir el tiempo requerido para resolver consultas analíticas:
```python
# Consulta: Total de tardanzas por trabajador
query = "SELECT id_trabajador, COUNT(*) as tardanzas FROM df WHERE estado_asistencia = 'Tardanza' GROUP BY id_trabajador"

# Lectura y ejecución sobre CSV
t0 = time.perf_counter()
spark.read.option("header", "true").csv("/tmp/exp05/csv").filter("estado_asistencia = 'Tardanza'").groupBy("id_trabajador").count().collect()
t_csv_r = time.perf_counter() - t0

# Lectura y ejecución sobre Parquet
t0 = time.perf_counter()
spark.read.parquet("/tmp/exp05/parquet").filter("estado_asistencia = 'Tardanza'").groupBy("id_trabajador").count().collect()
t_parquet_r = time.perf_counter() - t0

# Lectura y ejecución sobre Delta
t0 = time.perf_counter()
spark.read.format("delta").load("/tmp/exp05/delta").filter("estado_asistencia = 'Tardanza'").groupBy("id_trabajador").count().collect()
t_delta_r = time.perf_counter() - t0
```

### Paso 4: Exportación de Resultados
Guardar la tabla comparativa con los resultados consolidados en `archivos-csv/tiempos_formatos.csv`.

---

## 5. Entregables y Evidencias
- [ ] Capturas en `capturas/` mostrando las carpetas de salida, tamaños en bytes (`dbutils.fs.ls`) y las celdas de tiempo.
- [ ] Exportar `archivos-csv/tiempos_formatos.csv` con columnas: `Formato`, `TiempoEscritura_s`, `TiempoLectura_s`, `EspacioDisco_KB`, `FactorCompresion`.

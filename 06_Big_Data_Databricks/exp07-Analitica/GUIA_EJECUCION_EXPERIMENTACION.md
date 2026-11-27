# Guía de Ejecución de la Experimentación: EXP-07 Analítica Avanzada

## 1. Identificación y Objetivos
- **Código de Experimento:** `EXP-07`
- **Nombre:** Analítica Avanzada y Cálculo de KPIs en Databricks / Spark SQL.
- **Módulo:** `06_Big_Data_Databricks/exp07-Analitica`
- **Objetivo Principal:** Ejecutar consultas analíticas avanzadas, joins de gran volumen y cálculo distribuido de los KPIs clave del sistema de remuneraciones y desempeño laboral (TPA, ICT, TDT, IEP), validando la paridad de resultados con el modelo dimensional de Power BI y SQL Server.

---

## 2. Estructura del Directorio
```
exp07-Analitica/
├── README.md                           <- Esta guía de ejecución
├── GUIA_EJECUCION_EXPERIMENTACION.md   <- Copia de la guía de ejecución
├── capturas/                           <- Evidencias de dashboards, visualizaciones y KPIs
└── archivos-csv/                       <- CSVs con KPIs consolidados y matrices de resultados
```

---

## 3. Fórmulas de KPIs Analizados

1. **Tasa de Puntualidad en Asistencias (TPA):**
   $$\text{TPA} = \frac{\text{Asistencias Puntuales}}{\text{Total de Asistencias}} \times 100$$
2. **Índice de Cumplimiento de Tareas (ICT):**
   $$\text{ICT} = \frac{\text{Tareas Completadas}}{\text{Total de Tareas Asignadas}} \times 100$$
3. **Tasa de Descuento por Tardanza (TDT):**
   $$\text{TDT} = \frac{\text{Asistencias con Tardanza}}{\text{Total de Asistencias}} \times 100$$
4. **Índice de Eficiencia del Personal (IEP):**
   $$\text{IEP} = 0.5 \times \text{TPA} + 0.5 \times \text{ICT}$$

*Valores de referencia esperados (escala base 582): TPA = 92.10%, ICT = 56.36%, TDT = 3.44%, IEP = 75.12.*

---

## 4. Procedimiento de Ejecución Paso a Paso

### Paso 1: Creación de Vistas Temporales en Spark SQL
```python
df_asistencias.createOrReplaceTempView("v_asistencias")
df_tareas.createOrReplaceTempView("v_tareas")
```

### Paso 2: Consulta Distribuida de KPIs Globales
```sql
-- Ejecución en Celda SQL de Databricks
WITH kpi_asistencias AS (
    SELECT 
        COUNT(*) as total_asistencias,
        SUM(CASE WHEN estado_asistencia = 'Puntual' THEN 1 ELSE 0 END) as puntuales,
        SUM(CASE WHEN estado_asistencia = 'Tardanza' THEN 1 ELSE 0 END) as tardanzas
    FROM v_asistencias
),
kpi_tareas AS (
    SELECT 
        COUNT(*) as total_tareas,
        SUM(CASE WHEN estado_tarea = 'Completada' THEN 1 ELSE 0 END) as completadas
    FROM v_tareas
)
SELECT 
    ROUND((puntuales * 100.0) / total_asistencias, 2) as TPA,
    ROUND((completadas * 100.0) / total_tareas, 2) as ICT,
    ROUND((tardanzas * 100.0) / total_asistencias, 2) as TDT,
    ROUND((0.5 * ((puntuales * 100.0) / total_asistencias)) + (0.5 * ((completadas * 100.0) / total_tareas)), 2) as IEP
FROM kpi_asistencias, kpi_tareas;
```

### Paso 3: Agregación Multidimensional por Trabajador y Mes
Generar la matriz de rendimiento individual para consolidar en la capa Gold:
```python
df_kpi_trabajador = spark.sql("""
    SELECT 
        a.id_trabajador,
        date_format(a.fecha, 'yyyy-MM') as anio_mes,
        COUNT(DISTINCT a.id_asistencia) as total_asistencias,
        SUM(CASE WHEN a.estado_asistencia = 'Puntual' THEN 1 ELSE 0 END) as asistencias_puntuales,
        COUNT(DISTINCT t.id_tarea) as total_tareas,
        SUM(CASE WHEN t.estado_tarea = 'Completada' THEN 1 ELSE 0 END) as tareas_completadas
    FROM v_asistencias a
    LEFT JOIN v_tareas t 
        ON a.id_trabajador = t.id_trabajador AND a.fecha = t.fecha
    GROUP BY a.id_trabajador, date_format(a.fecha, 'yyyy-MM')
""")
```

### Paso 4: Exportación de Resultados
Guardar la matriz de resultados en `archivos-csv/kpi_calculados_databricks.csv`.

---

## 5. Entregables y Evidencias
- [ ] Captura de las visualizaciones generadas en Databricks (gráficos de barras y tablas) en `capturas/`.
- [ ] Archivo `archivos-csv/kpi_calculados_databricks.csv` con los cálculos obtenidos por escala.

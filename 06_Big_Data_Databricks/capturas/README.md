# Capturas del experimento EXP-02 (carga y consulta a tres escalas): qué muestra cada una

Notebook `EXP02_Databricks_Rendimiento`, ejecutado el 21/11/2026 en Databricks Free Edition (serverless).
Escalas: 582 filas (datos reales del Data Mart), 5 000 y 10 000 filas (sintéticos, semilla 2026).

| Captura | Qué muestra | Qué se evalúa / cómo leerla |
|---|---|---|
| **D-01** · `D-01_esquema_volumen_directorio.png` | Esquema `bd_rendimiento`, volumen `vol_rendimiento` y carpetas `datos_base` y `resultados` en Unity Catalog (celda 5). | Que el entorno de almacenamiento quedó preparado. |
| **D-02** · `D-02_csv_en_volumen_sha256.png` | Los seis CSV en el volumen con sus bytes y su huella SHA-256 (celda 9). | Integridad: las seis huellas coinciden con el manifiesto, es decir, se usaron exactamente los archivos del repositorio. |
| **D-03** · `D-03_head_archivos.png` | Primeras líneas de `asistencias_base.csv` y `tareas_base.csv` (celdas 11 y 12). | Formato de los archivos: encabezado, separador y que solo hay IDs (sin nombres ni datos personales). |
| **D-04** · `D-04_dataframes.png` | DataFrames `dfAsistencias` y `dfTareas` con esquema explícito y primeras filas (celda 14). | Que Spark lee los CSV con los tipos correctos. |
| **D-05** · `D-05_display_por_mes.png` | Tabla de asistencias por mes y estado (celda 16). | Julio 188 a tiempo / 15 tardanzas, agosto 171 / 15, septiembre 177 / 16: totales 203, 186 y 193, iguales al Data Mart. |
| **D-05b** · `D-05b_grafico_barras.png` | La misma tabla como gráfico de barras: mes en el eje X, cantidad en el eje Y, estado por color. | Evalúa visualmente la puntualidad por mes: en los tres meses la gran mayoría llega a tiempo y las tardanzas son pocas y parecidas. |
| **D-06** · `D-06_tablas_esquema.png` | Tablas Delta `tb_asistencias` y `tb_tareas` guardadas en el esquema (celda 19). | Persistencia de la escala base. |
| **D-07** · `D-07_group_by_y_kpi_base.png` | `COUNT + GROUP BY` por estado y KPI de la línea base (celda 21). | 536 a tiempo / 46 tardanzas; 401 completadas / 100 en progreso / 81 asignadas; TPA 92,10, ICT 56,36, TDT 3,44, IEP 75,12, iguales a Power BI. |
| **D-08** · `D-08_escala_5000.png` | Escala de 5 000 filas: contenido de los CSV, conteo, tablas y GROUP BY (celda 24). | Que la escala sintética se cargó completa (5 000 filas por tabla). |
| **D-08b** · `D-08b_escala_10000.png` | Escala de 10 000 filas: conteo y GROUP BY (celda 24). | Que la escala mayor se cargó completa (10 000 filas por tabla). |
| **D-09** · `D-09_entorno_spark.png` | Entorno de ejecución: edición, Spark 4.2.0, runtime `client.6.6`, Python 3.12.3 (celda 26). | Condiciones de prueba del experimento (necesarias para reproducirlo). |
| **T-01** · `T-01_csv_tiempos_y_resumen.png` | CSV con las 72 mediciones (12 combinaciones × 6) y el resumen con mediana, mínimo y máximo (celda 30). | Los datos crudos del experimento: 1 calentamiento + 5 repeticiones por escala y operación. |
| **T-02** · `T-02_registro_RUN_y_kpi_por_escala.png` | Registro de ejecuciones RUN-03 a RUN-05 y KPI por escala (celda 32). | Trazabilidad de cada corrida y que los KPI de cada escala coinciden con el manifiesto del generador. |
| **T-03** · `T-03_grafico_tiempo_vs_filas.png` | Gráfico de tiempo (segundos) frente a filas por tabla: carga (CSV → Delta) y consulta (GROUP BY). Puntos = mediana; barras = mínimo y máximo. | **Resultado del experimento**: al pasar de 582 a 10 000 filas los tiempos no subieron (carga 1,78–2,29 s; consulta 0,55–0,66 s). En este rango pesa más el costo fijo de cada operación que el volumen. No se extrapola fuera de 582–10 000 filas. |

## Qué demuestran los gráficos

**D-05b · Asistencias por mes y estado.** La Figura D-05b muestra cuántas asistencias hubo en cada mes, separando las que llegaron a tiempo de las tardanzas. En los tres meses la gran mayoría del personal llega a tiempo y las tardanzas son pocas y parecidas: 15 de 203 en julio (7,39 %), 15 de 186 en agosto (8,06 %) y 16 de 193 en septiembre (8,29 %). Lo que se quiere demostrar es que la puntualidad es estable durante el trimestre, con una leve tendencia a empeorar mes a mes (la TPA baja de 92,61 % a 91,71 %). Además, los totales por mes coinciden con los del Data Mart, lo que confirma que Databricks leyó el mismo conjunto de datos que Power BI.

**T-03 · Tiempo frente a filas (resultado del experimento).** El gráfico responde a la pregunta del experimento: ¿cuánto más tarda Databricks si hay más datos? En el eje horizontal está el número de filas (582, 5 000 y 10 000) y en el vertical los segundos; cada punto es la mediana de cinco repeticiones y las barras muestran el mínimo y el máximo. Las líneas son casi planas e incluso bajan un poco: cargar 10 000 filas (1,78 s) no tomó más que cargar 582 (2,29 s), y las consultas se mantienen entre 0,55 y 0,66 s. Lo que demuestra es que, con estos volúmenes, el tiempo lo determina el costo fijo de arrancar cada operación en Spark y no la cantidad de datos; Spark tiene margen para crecer sin que el usuario note demoras. No se puede afirmar lo mismo para millones de filas, porque no se midieron.

# Capturas de la solución Medallion: qué muestra cada una

Notebook `BigData_Solucion_Medallion`, ejecutado el 26/11/2026 en Databricks Free Edition (serverless).
Cada salida del notebook imprime el código de la captura, la fecha y hora de Lima y el responsable (Luis Obregón Hidalgo).
"Escala base" = los 582 registros reales del Data Mart; "5 000" y "10 000" = datos sintéticos (semilla 2026).

| Captura | Qué muestra | Qué se evalúa / cómo leerla |
|---|---|---|
| **S-01** · `S-01_esquemas_medallion.png` | Creación de los esquemas `mon_bronze`, `mon_silver` y `mon_gold` en el catálogo `workspace`, y la versión de Spark y Python. | Que existe la estructura de tres capas antes de cargar datos. |
| **S-02** · `S-02_bronze_ingesta.png` | Esquema de la tabla Bronze (todas las columnas como texto + `_escala`, `_archivo_origen`, `_fecha_ingesta`) y conteo de filas por escala y archivo. | Que la ingesta cargó todo sin alterar el dato: 582, 5 000 y 10 000 filas por tabla, cada grupo con su archivo de origen. |
| **S-03a** · `S-03a_eda_describe_summary.png` | `describe()` de asistencias y `summary()` de tareas (conteo, mínimo, cuartiles, máximo) en la escala base. | Primera mirada a los datos: rangos de IDs y de fechas, que no hay valores fuera de lo esperado. |
| **S-03b** · `S-03b_eda_nulos_distintos.png` | Por cada columna: filas, nulos o vacíos, % de nulos y valores distintos (escala base). | Calidad de origen. Asistencias: 0 nulos. Tareas: `Fecha_Inicio` 81 vacíos (13,92 %), `Fecha_Entrega` 181 (31,10 %), `Observaciones` 509 (87,46 %). Son vacíos esperados: una tarea *Asignada* aún no tiene inicio ni entrega, y la mayoría de tareas no lleva observación. |
| **S-04a** · `S-04a_eda_distribuciones_estado.png` | Asistencias por estado (cantidad y %) y tareas por estado, con cuántas tienen observación y cuántas dicen "FUERA DE PLAZO". | Distribución de los datos que alimentan los KPI: 536 a tiempo (92,1 %) y 46 tardanzas; 401 completadas, 100 en progreso, 81 asignadas. |
| **S-04b** · `S-04b_eda_mes_hora_entrada.png` | Asistencias por mes y estado, y estadísticos de la hora de entrada (en minutos desde las 00:00). | Que los tres meses tienen volumen parecido (203 / 186 / 193, igual que el Data Mart) y en qué rango horario llega el personal. |
| **S-04c** · `S-04c_eda_registros_por_trabajador.png` | Número de registros por trabajador (ID). | Balance entre trabajadores: siete tienen 66 registros y los IDs 2, 9 y 11 tienen 40. Explica por qué los KPI se calculan con proporciones y no con conteos. |
| **S-05** · `S-05_diagnostico_calidad.png` | Tabla de 15 reglas de calidad (IDs no numéricos, fechas inválidas, salida antes que entrada, estado fuera de catálogo, estado que no cumple la regla de las 09:41, duplicados, etc.) con las filas que incumplen cada una, por escala. | Calidad **antes** de limpiar. Escala base: 0 incumplimientos. Sintéticos: "Completada sin fecha de entrega" 142 (5 000) y 300 (10 000); "En Progreso sin fecha de inicio" 30 y 55. |
| **S-06a** · `S-06a_silver_decisiones_esquema.png` | Las 8 decisiones de limpieza y el esquema Silver resultante (columnas renombradas a minúscula y con su tipo: entero, timestamp, fecha). | Que la limpieza usa `select`, `withColumnRenamed`, `cast`, `trim`, `na.drop`, `na.fill`, `dropDuplicates` y `filter`, y que el resultado queda tipado. |
| **S-06b** · `S-06b_silver_muestras.png` | Cinco filas de ejemplo de asistencias y de tareas ya limpias en Silver, con las columnas derivadas (mes, día, minuto de entrada, banderas). | Cómo queda el dato listo para calcular indicadores. |
| **S-07** · `S-07_conciliacion_cuarentena.png` | Filas en Bronze vs Silver por escala y tareas enviadas a cuarentena por tipo de alerta. | Que la limpieza no perdió filas (0 descartadas en las tres escalas) y que 527 tareas sintéticas con errores quedaron marcadas en `tareas_cuarentena` en lugar de borrarse. |
| **S-08** · `S-08_gold_kpi_global_y_mes.png` | Tablas Gold `kpi_global` y `kpi_mes`: asistencias, puntuales, tareas, sin observación, fuera de plazo, TPA, ICT, TDT e IEP por escala y mes. | Los indicadores finales. Escala base por mes (TPA / ICT / TDT / IEP): jul 92,61 / 57,14 / 3,45 / 75,67 · ago 91,94 / 57,53 / 3,76 / 75,59 · sep 91,71 / 54,40 / 3,11 / 74,09. |
| **S-09** · `S-09_validacion_powerbi_kpi_trabajador.png` | Comparación KPI Gold vs Power BI y ranking de trabajadores por IEP (escala base). | **Prueba de aceptación**: TPA 92,10, ICT 56,36, TDT 3,44, IEP 75,12 iguales a Power BI (diferencia 0, columna `coincide = true`). El ranking va de IEP 96,00 (ID 2) a 22,00 (ID 9). |
| **S-10a** · `S-10a_visualizaciones.png` | La celda de visualizaciones dentro del notebook (código de captura y gráficos). | Evidencia de que los gráficos se generaron en Databricks. |
| **S-10b** · `S-10b_graficos_gold.png` | Los cuatro gráficos de la capa Gold (detalle abajo). | Ver sección siguiente. |
| **S-11** · `S-11_persistencia_tablas_delta.png` | Inventario de las 10 tablas Delta (capa, filas, bytes, comentario) e historial de versiones de una tabla Gold. | Que todo quedó guardado como tablas Delta documentadas: Bronze y Silver con 15 582 filas por tabla; Gold con 3, 9, 267 y 800 filas. |
| **S-12a** · `S-12a_dashboard_superior.png` | Dashboard publicado "BASAV · Monitoreo de empleados (Gold)" en Databricks. | Ver sección siguiente. |

## Qué evalúa cada gráfico (S-10b)

1. **KPI por mes (arriba izquierda)** — líneas de TPA, ICT, TDT e IEP en julio, agosto y septiembre (datos reales).
   Evalúa si el rendimiento del equipo cambia en el tiempo. Resultado: los cuatro indicadores son estables; el ICT baja de 57,5 a 54,4 en septiembre.
2. **IEP por trabajador (arriba derecha)** — barras horizontales con el índice de eficiencia de cada trabajador (ID), ordenadas.
   Evalúa quién tiene mejor y peor desempeño combinado (0,3·TPA + 0,5·ICT + 0,2·(100 − TDT)). Va de 96,0 (ID 2) a 22,0 (ID 9); es la base del bono referencial.
3. **Hora de entrada (abajo izquierda)** — histograma de las horas de llegada, en azul las asistencias "A tiempo" y en naranja las "Tardanza", con una línea en las 09:41.
   Evalúa si la regla de puntualidad se aplica bien: todas las barras azules están antes de la línea y todas las naranjas después.
4. **KPI Gold por escala de datos (abajo derecha)** — barras agrupadas de TPA, ICT, TDT e IEP para 582, 5 000 y 10 000 filas.
   Evalúa que el pipeline da resultados coherentes al aumentar el volumen. Los sintéticos quedan cerca de la base porque copian el comportamiento de los trabajadores reales; no describen personas reales.

## Qué muestra el dashboard (S-12a)

- **Seis tarjetas**: TPA 92,1 %, ICT 56,36 %, TDT 3,44 %, IEP 75,12, 582 asistencias y 582 tareas (datos reales). Son los mismos valores del tablero de Power BI.
- **KPI por mes**: líneas de los cuatro indicadores por mes (mismo contenido que el gráfico 1).
- **IEP por trabajador**: barras por ID (mismo contenido que el gráfico 2).
- **KPI por escala de datos**: barras agrupadas por escala (mismo contenido que el gráfico 4).
- **Tareas en cuarentena por escala**: cuántas tareas sintéticas tienen alerta de calidad y de qué tipo (complementa S-07).

El dashboard lee directamente las tablas `workspace.mon_gold` y `workspace.mon_silver.tareas_cuarentena`, así que se actualiza si se vuelve a ejecutar el notebook.

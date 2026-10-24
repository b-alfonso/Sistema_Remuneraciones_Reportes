# Registro de cambios

## Etapa 1 — Origen transaccional

- Rama: `feature/estructura-datos`.
- Commit: `16b8f18`.
- Se crearon las cuatro carpetas del proyecto y el script de estructura y datos.
- Se incluyeron las tablas del esquema, claves foráneas y generación repetible del trimestre julio–septiembre de 2026.
- Se publicó el mismo estado inicial en `main` y en la rama de trabajo.
- Validación en el entorno de desarrollo: análisis sintáctico T-SQL y cálculo independiente del calendario. El usuario confirmó la creación de la base en su instancia de SSMS; no se adjuntaron todavía evidencias de sus cantidades ni resultados.

## Etapa 2 — Data Mart, ETL y reportes

- Rama: `feature/etl-reportes`.
- Se añadió `02_Creacion_Data_Mart.sql` con cuatro dimensiones, hechos, bitácora y rechazos.
- Se añadió `02_Procedimiento_ETL.sql` con intervalo parametrizado, limpieza, validación, carga transaccional y repetición sin duplicar medidas.
- Se añadieron las vistas SQL, medidas DAX y documentación de conexión, modelo y demostración.
- Se añadió un script ejecutable de conciliación e idempotencia para SSMS.
- Se documentaron las limitaciones del origen: aprobación inferida, asistencia sin proyecto, jornada contractual no historizada y ausencia de datos salariales.
- No se modificó el generador OLTP que el usuario ya ejecutó.
- Validación: los cinco scripts SQL se ejecutaron correctamente en una instancia aislada de SQL Server 2022 Developer. Se comprobó repetición del origen, reinstalación del Data Mart, conciliación, idempotencia y carga parcial.
- Se verificaron normalización de textos, rechazo de estados desconocidos y salidas incoherentes, frontera de las 09:41 y tareas de varios proyectos en una misma jornada sin multiplicar asistencias. Después se restauraron los datos iniciales de esa instancia aislada.
- En esta etapa se guardaron resultados de ejecución y quedó pendiente construir el `.pbix`. Las evidencias antiguas fueron sustituidas por `Evidencias/03_Resultados_Padron_Origen.txt`; el estado actual del informe se registra en la etapa 6.

## Etapa 3 — Scripts y organización de entregables

- Rama: `feature/simplificar-scripts`.
- Se respetó la eliminación del README principal realizada en GitHub.
- La creación del Data Mart utiliza `CREATE DATABASE` y `CREATE TABLE` directos, con claves primarias, foráneas y unicidad. Este archivo se ejecuta una sola vez.
- Se retiraron las instrucciones de sesión `ANSI_NULLS` y `QUOTED_IDENTIFIER` de los scripts del proyecto. No se modificó el origen.
- El ETL utiliza un calendario con `WHILE` y `CASE`, sin SQL dinámico ni bloqueo de aplicación. Mantiene la limpieza, el registro de rechazos y la carga transaccional del intervalo.
- Las vistas SQL se trasladaron a `02_Procedimientos_Almacenados` y las medidas DAX a `04_Documentacion`. `03_Vistas_PowerBI` queda reservada para el dashboard y sus exportaciones.
- Se simplificaron las consultas de validación y evidencia, y se añadió una guía de ejecución sin recrear el README principal.
- Se generó `Modelo_Estrella.svg` a partir de las tablas y relaciones de SQL Server. Se añadió una guía para guardar el diagrama en SSMS y subir una captura real.
- Validación: actualización del procedimiento y las vistas sobre una instalación anterior, creación del Data Mart nuevo, cargas repetidas y comparación de los treinta resúmenes mensuales. Las cantidades e indicadores coinciden con la versión anterior. Se verificaron de nuevo los controles de calidad y la carga parcial.
- Los resultados de esta etapa fueron sustituidos por la evidencia vigente del padrón. La entrega del `.pbix` y la captura de SSMS se registran en la etapa 6.

## Etapa 4 — Padrón de trabajadores

- Rama: `feature/personal-origen`.
- Se alinearon nombres, identificadores de empleado y trabajador, cargos, códigos y roles con el padrón original proporcionado.
- Se añadió `01_Base_Datos/03_Alinear_Personal_Origen.sql` para actualizar las instalaciones existentes sin eliminar asistencias ni tareas. El trabajador 5 conserva el histórico del registro anterior correspondiente.
- Se actualizó el generador para nuevas instalaciones. No se copian del archivo adjunto PIN, correos ni teléfonos.
- El ETL identifica las jornadas de practicantes mediante los trabajadores 2, 9 y 11, porque el origen solo distingue trabajador y administrador.
- Se actualizaron las evidencias y la guía completa. La validación muestra diez personas y treinta resúmenes mensuales; los resultados vigentes están en `Evidencias/03_Resultados_Padron_Origen.txt`.
- Se añadió una página propuesta de bono por efectividad con base y porcentaje referenciales explícitos, junto con sus medidas DAX. Los visuales y las medidas quedan pendientes de comprobar en Power BI Desktop.
- Comprobación en SQL Server: conservación de identificadores de asistencia y tarea, fechas y estados; segunda ejecución de la alineación sin duplicados; recarga del Data Mart con el padrón de origen.

## Etapa 5 — Lectura de indicadores

- Se añadió un diccionario de tarjetas y medidas auxiliares con fórmulas, interpretación y sentido de mejora.
- Se documentó la lectura de los filtros y el ejemplo de Edu Cruz en septiembre: 22 asistencias, 22 tareas, ICT 59,09% e IEP 79,55.
- Se incluyeron frases de apoyo para la demostración y la distinción entre cumplimiento sin observaciones, finalización y entrega fuera de plazo.
- No se modificaron los scripts SQL ni las medidas DAX.

## Etapa 6 — Informe y evidencias de entrega

- Se incorporó el informe construido por el equipo con las páginas **Rendimiento del personal** y **Bono por efectividad**.
- Se dejó una única versión de entrega, `03_Vistas_PowerBI/Reporte_Rendimiento_Personal.pbix`, conservando sin cambios el contenido del archivo completo. La copia anterior del mismo nombre tenía una sola página sin visuales.
- Se reunieron las capturas existentes en `Evidencias`, se normalizó el nombre de la captura de rendimiento y se retiró una copia idéntica de la validación que estaba fuera de esa carpeta.
- Se resumieron las guías con pasos directos y sin emojis. Se actualizaron al alcance de dos páginas y al tiempo de cinco minutos de PPT y diez de demostración. Las ampliaciones de asistencia y proyectos son opcionales.
- Se inspeccionó la estructura guardada del `.pbix`: dos páginas, seis tarjetas y un gráfico de barras en rendimiento, y dos tablas con filtros superior/inferior por IEP en bono. No se ejecutó Power BI Desktop ni se validó una conexión en vivo durante esta revisión.
- Faltan las capturas `06_Modelo_PowerBI.png` y `10_Bono_Referencial.png`. El guion detallado queda para el viernes.

## Registro de aportes y evidencias

Después de cada aporte real, agregar una entrada con integrante, archivos, cambio, validación y referencia al commit o pull request. Las revisiones se registran desde la cuenta de quien las realiza.

## Etapa 7 — Informe BI y correspondencia de evidencias

- Se tomó como referencia la solución publicada en `9726a54`: julio–septiembre de 2026, diez trabajadores y 582 movimientos de asistencia y tareas.
- Se preparó el informe de T2 con arquitectura, modelo, ETL, indicadores, validaciones, resultados y conclusiones respaldados por el repositorio.
- Se sustituyeron las imágenes del otro modelo por las capturas existentes de SSMS y Power BI. El diagrama de arquitectura se elaboró a partir de los scripts actuales.
- Se añadieron el manifiesto de evidencias y enlaces permanentes a código, resultados, reportes e historial. Los apartados de Big Data quedan reservados, salvo el objetivo futuro de 1.3.
- Se corrigieron las guías que aún indicaban que faltaba la captura de relaciones; ya está en `03_Vistas_PowerBI/06_Modelo_PowerBI.png`.
- Se documentó que las dos copias PBIX publicadas tienen el mismo contenido. Se conservan ambas y se identifica `Reporte_Rendimiento_Personal.pbix` como archivo principal.
- No se modificaron los scripts SQL, las medidas DAX, los PBIX ni las imágenes existentes. No se realizó una nueva ejecución de SQL Server o Power BI durante la revisión documental.
- La captura complementaria del bono todavía no está publicada. El informe usa su tabla de resultados y el archivo PBIX, sin presentar una captura inexistente.

## Etapa 8 — Carga de la simulación en otra computadora

- Se añadieron `01_Base_Datos/04_Cargar_Simulacion.sql` para ejecutar el ETL y `05_Comprobar_Simulacion.sql` para consultar servidor, cantidades, cargas, indicadores y duplicados.
- El cargador avisa cuando falta el procedimiento o no existen movimientos del trimestre. No inserta hechos manualmente ni elimina bases.
- Se aclaró que crear el OLTP y el Data Mart deja los hechos vacíos hasta ejecutar el procedimiento. Se actualizaron el orden de ejecución y la guía general, y se añadió una guía para otra computadora.
- Se comprobó la instalación desde cero en SQL Server 2022 Developer aislado: tabla vacía tras el DDL, carga de 1.164 filas, 582 asistencias, 582 tareas, diez trabajadores y treinta resúmenes mensuales.
- Se verificó que el generador y el ETL pueden repetirse sin acumular medidas. Una carga con origen vacío se detuvo y conservó los hechos anteriores. Los resultados están en `Evidencias/Resultados_Carga_Simulacion.txt`.
- Se corrigió el enlace del modelo estrella para usar la captura existente, porque el SVG enlazado ya no estaba en la versión actual.
- Se reconocieron las capturas de rendimiento y bono ya publicadas en `03_Vistas_PowerBI`. No se modificaron sus imágenes ni los archivos PBIX.
- Esta revisión ejecutó SQL Server y revisó la estructura de los PBIX; no abrió Power BI Desktop ni probó su conexión en vivo.

## Etapa 9 — Guía unificada para la replicación y demostración

- Se reunieron los contenidos de `09_Guia_Completa.md` y `14_Simulacion_Otra_Computadora.md` en el archivo 09, ampliados con instrucciones para personas sin experiencia en GitHub, SQL Server o Power BI.
- Se detallaron instalación, descarga sin Git, conexión, ejecución de archivos completos, creación y carga, comprobaciones y diagnóstico de errores.
- Se incluyeron dos recorridos de Power BI: abrir el PBIX terminado y construir desde cero con relaciones, medidas DAX, formato, tarjetas, segmentadores, barras y tablas del bono.
- Las trece definiciones DAX del recorrido se copiaron de sus archivos canónicos. Se añadieron ejemplos de resultados, guardado, evidencias y creación de un pull request desde el navegador.
- Se documentó el ensayo de hasta diez minutos de demostración, separado de los cinco minutos del PPT y de la instalación previa de programas.
- El archivo 14 conserva un enlace al 09. Se actualizaron los resúmenes para señalar una única guía principal.
- Verificación documental: enlaces locales, anclas, orden de los seis SQL, fórmulas y cantidades frente al código y evidencias existentes. No se modificaron SQL, DAX, PBIX, imágenes ni informes Word/PDF; no se presenta una nueva ejecución de SQL Server o Power BI como parte de esta revisión.

## Ubicación y recorrido de la guía de replicación

- La guía completa se trasladó a `05_Procedimientos_Replicacion/09_Guia_Completa.md`.
- El recorrido comienza en la creación de las bases y continúa con numeración desde el apartado 1.
- Se conservaron tablas, enlaces, instrucciones de clic derecho y resultados de comprobación; se retiraron los apartados de preparación y diagnóstico.
- Se actualizaron los enlaces desde la documentación.

## Conexión e importación de Power BI

- Se documentaron dos recorridos: descargar el PBIX terminado o construir los dashboards desde un informe en blanco.
- La guía utiliza Importar y el servidor `.` para la instancia local predeterminada.
- Se detallaron la detección automática y comprobación de las cuatro relaciones, además de la actualización de datos después del ETL.
- Los archivos PBIX, scripts SQL y capturas se conservan sin cambios.

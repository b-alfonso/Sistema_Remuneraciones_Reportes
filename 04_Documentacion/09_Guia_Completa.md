# Guía completa: instalar, cargar los datos y crear los dashboards

Esta es la guía principal y unificada del proyecto. Reúne la instalación, la simulación en otra computadora, la construcción de los reportes y la demostración. Sustituye el contenido anterior de `09_Guia_Completa.md` y `14_Simulacion_Otra_Computadora.md`.

El objetivo es llegar desde una computadora sin el proyecto instalado hasta un reporte que muestre los resultados del trimestre **julio–septiembre de 2026**. No es necesario saber Git ni escribir comandos de GitHub. Los pasos de instalación están orientados a Windows, que es el entorno de las capturas del equipo.

> Los programas se instalan y la conexión se ensaya antes de la exposición. Los cinco minutos del PPT y los diez minutos de demostración no incluyen descargar programas o instalar SQL Server.

## Índice

1. [Qué vamos a construir y qué significa cada herramienta](#conceptos)
2. [Qué necesitas y cómo instalarlo](#preparacion)
3. [Descargar el repositorio desde GitHub](#descarga)
4. [Conectarse a SQL Server y ejecutar un archivo](#ssms)
5. [Elegir el punto de inicio](#inicio)
6. [Crear las bases, instalar el ETL y cargar los datos](#instalacion)
7. [Comprobar cantidades e indicadores](#comprobacion)
8. [Dibujar el modelo estrella en SSMS](#estrella)
9. [Abrir el reporte terminado en Power BI](#reporte-existente)
10. [Construir el reporte desde una página vacía](#reporte-nuevo)
11. [Crear las medidas y darles formato](#medidas)
12. [Crear tarjetas, filtros y barras](#rendimiento)
13. [Crear la página del bono referencial](#bono)
14. [Guardar, documentar y subir evidencias](#entrega)
15. [Realizar la demostración en diez minutos](#demostracion)
16. [Resolver errores frecuentes](#errores)
17. [Lista final y límites de la simulación](#final)

<a id="conceptos"></a>
## 1. Qué vamos a construir y qué significa cada herramienta

| Nombre | Explicación para esta guía |
| --- | --- |
| GitHub | Sitio donde están los archivos del proyecto. Descargar el código no crea bases en tu computadora. |
| Repositorio | Carpeta del proyecto publicada en GitHub. Contiene SQL, reportes, documentación y capturas. |
| SQL Server | Programa que almacena los datos y ejecuta las consultas y procedimientos. Su servicio debe estar iniciado. |
| Instancia o servidor | Instalación concreta de SQL Server a la que te conectas. Debes usar la misma en SSMS y Power BI. |
| SSMS | SQL Server Management Studio: aplicación con la que abres los archivos SQL y los ejecutas en el servidor. Instalar solo SSMS no instala el motor SQL Server. |
| OLTP | Base con los registros de trabajadores, asistencias y tareas. Aquí se llama `A&SG_OLTP`. |
| ETL | Proceso de extraer, transformar y cargar. El procedimiento toma datos del OLTP, limpia textos, valida registros y los carga en el destino. |
| Procedimiento almacenado | Código guardado dentro de SQL Server. Crear su definición no lo ejecuta. Debe invocarse con `EXEC`. |
| Data Mart | Base preparada para analizar resultados. Aquí se llama `A&SG_DataMart`. |
| Dimensiones | Tablas que describen trabajador, tiempo, proyecto y administrador. |
| Hechos | Cantidades de asistencia y tareas en `fac_rendimiento_kpis`. |
| Vista SQL | Consulta guardada que Power BI puede utilizar como fuente. Los nombres del proyecto comienzan por `vw_`. |
| Power BI Desktop | Aplicación donde se construyen tarjetas, tablas, filtros y gráficos. |
| Medida DAX | Fórmula de Power BI que se calcula según los filtros seleccionados. |
| PBIX | Archivo del reporte de Power BI, con modelo, medidas y visuales. Puede necesitar conexión al SQL Server para mostrar o actualizar sus datos. |

El recorrido es:

```text
A&SG_OLTP → procedimiento ETL → A&SG_DataMart → vistas SQL → Power BI
```

La simulación utiliza diez trabajadores, un administrador independiente y movimientos generados para el trimestre. Los movimientos son académicos; los nombres conservados del padrón no se declaran ficticios ni anónimos. MySQL, Clever Cloud y Streamlit son antecedentes técnicos: no necesitas conectarte a ellos para ejecutar esta entrega.

<a id="preparacion"></a>
## 2. Qué necesitas y cómo instalarlo

### 2.1 Revisar los programas

Abre el menú Inicio de Windows y busca:

1. **SQL Server Management Studio**.
2. **Power BI Desktop**.
3. **SQL Server Configuration Manager**, si está disponible, o **Servicios** para comprobar que existe un servicio de SQL Server.

Si ya utilizas SSMS, consigues conectarte y ejecutas consultas, el motor ya está disponible. No instales una segunda instancia solo para este proyecto. Si vas a usar la computadora de otra persona, solicita acceso a su instancia autorizada o prepara la tuya.

Descargas oficiales:

- [SQL Server Developer](https://www.microsoft.com/es-es/sql-server/sql-server-downloads).
- [Instalación de SQL Server Management Studio](https://learn.microsoft.com/es-es/ssms/install/install).
- [Power BI Desktop](https://www.microsoft.com/es-es/download/details.aspx?id=58494).

Las pantallas cambian según la versión. Sigue el instalador oficial. Las pruebas SQL conservadas en el repositorio se hicieron en **SQL Server 2022 Developer 16.0.4305.5**. No se exige cambiar el nivel de compatibilidad de la base.

### 2.2 Instalar SQL Server cuando todavía no existe

1. Descarga la edición **Developer**, destinada a desarrollo y aprendizaje.
2. Abre el instalador. Si Windows pide autorización para instalar, utiliza una cuenta con permiso.
3. Para una instalación local sencilla, utiliza la opción básica si tu instalador la ofrece; la personalizada permite elegir la instancia.
4. Anota el nombre de la instancia que indica el instalador. No inventes un nombre ni copies el de las capturas del equipo.
5. Conserva la información de conexión que muestre al finalizar.
6. Instala SSMS desde el enlace oficial si todavía no lo tienes.

No publiques contraseñas ni utilices una contraseña del ejemplo de otra persona. Para una instalación local propia, la autenticación de Windows suele ser la opción más sencilla si tu usuario fue autorizado durante la instalación.

### 2.3 Comprobar que el servicio está iniciado

1. Pulsa **Windows + R**.
2. Escribe `services.msc` y acepta.
3. Busca **SQL Server (MSSQLSERVER)** si instalaste la instancia predeterminada, o **SQL Server (nombre de tu instancia)** si elegiste una con nombre.
4. Comprueba que el estado sea **En ejecución**.
5. Si está detenido y tienes permiso, pulsa con el botón derecho y selecciona **Iniciar**.

SQL Server Agent no es necesario para esta simulación: la carga se ejecuta manualmente desde SSMS.

### 2.4 Instalar Power BI Desktop

1. Instala Power BI Desktop desde su descarga oficial o desde Microsoft Store.
2. Abre la aplicación al terminar.
3. Para trabajar localmente con el PBIX y SQL Server no hace falta publicar el reporte en Power BI Service.
4. Si abre una pantalla de bienvenida o inicio de sesión, continúa al entorno de Desktop cuando la aplicación permita trabajar localmente.

<a id="descarga"></a>
## 3. Descargar el repositorio desde GitHub

### 3.1 Descargar todo el proyecto

1. Abre [Sistema_Remuneraciones_Reportes](https://github.com/b-alfonso/Sistema_Remuneraciones_Reportes).
2. Comprueba que la rama seleccionada sea **main** para usar la versión integrada. Una rama de un pull request abierto todavía puede tener cambios pendientes de integración.
3. Pulsa el botón verde **Code**.
4. Selecciona **Download ZIP**.
5. Busca el ZIP en Descargas.
6. Pulsa con el botón derecho y elige **Extraer todo**.
7. Elige una carpeta que puedas encontrar, por ejemplo una carpeta del proyecto dentro de Documentos.
8. Abre la carpeta extraída. Debes ver `01_Base_Datos`, `02_Procedimientos_Almacenados`, `03_Vistas_PowerBI` y `04_Documentacion`.

No abras los archivos directamente dentro del ZIP. No necesitas instalar Git, clonar desde una terminal ni crear una cuenta de GitHub para descargar un repositorio público.

### 3.2 Si solo necesitas un archivo

En GitHub, abre el archivo y busca **Download raw file** o el botón de descarga. En archivos de texto también puedes utilizar **Raw** y guardar el contenido con la extensión correcta.

Un PBIX o una imagen debe descargarse como archivo; copiar el texto de su página de GitHub no sirve. Si Windows oculta extensiones, activa su visualización en el Explorador para comprobar que no guardaste `archivo.sql.txt`.

### 3.3 Entender las carpetas

| Carpeta | Para qué se utiliza |
| --- | --- |
| `01_Base_Datos` | Origen, creación del Data Mart, carga y comprobación. El archivo 03 es una corrección para instalaciones antiguas. |
| `02_Procedimientos_Almacenados` | Definición del ETL y vistas para Power BI. |
| `03_Vistas_PowerBI` | PBIX e imágenes de los reportes. Su nombre se conserva aunque no contenga los scripts de vistas. |
| `04_Documentacion` | Esta guía, reglas, DAX, validaciones y evidencias. |

No ejecutes todos los SQL solo por orden alfabético. El orden correcto combina archivos de dos carpetas y está detallado en el apartado 6.

<a id="ssms"></a>
## 4. Conectarse a SQL Server y ejecutar un archivo

### 4.1 Primera conexión en SSMS

1. Abre **SQL Server Management Studio**.
2. En la ventana de conexión, selecciona **Database Engine / Motor de base de datos** si pide el tipo de servidor.
3. Escribe el nombre de tu instancia. Ejemplos de formato: `localhost` para una instancia local predeterminada o `NOMBRE-PC\INSTANCIA` para una instancia con nombre. Son ejemplos; utiliza el nombre real de tu instalación.
4. Selecciona **Windows Authentication / Autenticación de Windows** si ese usuario tiene acceso.
5. Si tu instalación utiliza autenticación de SQL Server, emplea el usuario y contraseña autorizados para ella.
6. Pulsa **Connect / Conectar**.
7. A la izquierda debe aparecer el **Object Explorer / Explorador de objetos**, con el servidor y la carpeta **Databases / Bases de datos**.

Si el Explorador no aparece, busca **Ver → Explorador de objetos**. Si no conectas, consulta el apartado de errores antes de ejecutar archivos.

### 4.2 Anotar el servidor correcto

Pulsa **New Query / Nueva consulta**, pega y ejecuta:

```sql
SELECT SERVERPROPERTY('ServerName') AS servidor,
       CONVERT(varchar(40), SERVERPROPERTY('ProductVersion')) AS version_sql;
```

Anota el servidor devuelto. Ese es el que debes revisar después en Power BI. Cada integrante tiene su propia instancia y sus propias bases: los datos del compañero no aparecen automáticamente en tu equipo.

### 4.3 Cómo ejecutar cada archivo de esta guía

1. En SSMS, entra en **Archivo → Abrir → Archivo** o pulsa **Ctrl + O**.
2. Busca el SQL en la carpeta extraída del repositorio.
3. Ábrelo. Se mostrará en una pestaña de consulta.
4. Comprueba la conexión de esa pestaña en la barra de estado. Todas deben usar la misma instancia.
5. Haz clic en el editor y quita cualquier selección de texto. **F5 ejecuta solo lo seleccionado si dejaste una selección activa.**
6. Pulsa **F5** o **Execute / Ejecutar**.
7. Revisa las pestañas inferiores **Messages / Mensajes** y **Results / Resultados**.
8. Si aparece un error en rojo, detente, lee el primero y resuélvelo. No continúes acumulando errores de archivos que dependen del anterior.
9. Si termina correctamente, continúa con el siguiente archivo.

Los SQL contienen `USE` para elegir su base y `GO` para separar bloques. Se ejecutan en SSMS; no se pegan en Power BI ni en un editor MySQL.

<a id="inicio"></a>
## 5. Elegir el punto de inicio

| Situación | Qué hacer |
| --- | --- |
| Nunca instalé este proyecto. | Ejecutar los pasos 1 al 6 del apartado siguiente. |
| Solo ejecuté Estructura y Datos y Creación del Data Mart. | Continuar desde el paso 3. Que los hechos estén vacíos todavía es normal. |
| Ya tengo las bases, el procedimiento y las vistas vigentes. | Ejecutar los pasos 5 y 6 para recargar y comprobar. |
| Tengo datos cargados y solo quiero mostrar el reporte terminado. | Comprobar el paso 6 y seguir el apartado 9. |
| Quiero construir el dashboard desde cero. | Completar la carga y seguir los apartados 10 al 13. |
| Mi instalación antigua tiene nombres incorrectos o un esquema distinto. | Revisar [08_Padron_Trabajadores.md](08_Padron_Trabajadores.md). No borrar ni mezclar bases de otra versión. |

`02_Creacion_Data_Mart.sql` se ejecuta una sola vez por instalación. Si ya existe una base llamada `A&SG_DataMart`, no asumas que está vacía ni la elimines. Comprueba qué versión contiene antes de aplicar cambios. Si no puedes identificarla, pide ayuda al responsable de esa instalación.

<a id="instalacion"></a>
## 6. Crear las bases, instalar el ETL y cargar los datos

Mantén la misma instancia conectada durante todos los pasos. El número entre paréntesis es el orden de ejecución, no siempre el prefijo del archivo.

| Orden | Archivo que debes abrir | Qué debe ocurrir |
| --- | --- | --- |
| 1 | [01_Estructura_y_Datos.sql](../01_Base_Datos/01_Estructura_y_Datos.sql) | Crea y llena `A&SG_OLTP`. |
| 2 | [02_Creacion_Data_Mart.sql](../01_Base_Datos/02_Creacion_Data_Mart.sql) | Crea dimensiones, hechos y tablas de control. |
| 3 | [02_Procedimiento_ETL.sql](../02_Procedimientos_Almacenados/02_Procedimiento_ETL.sql) | Guarda la definición del procedimiento ETL. |
| 4 | [03_Vistas_PowerBI.sql](../02_Procedimientos_Almacenados/03_Vistas_PowerBI.sql) | Crea las vistas que consultará Power BI. |
| 5 | [04_Cargar_Simulacion.sql](../01_Base_Datos/04_Cargar_Simulacion.sql) | Ejecuta el ETL y llena el Data Mart. |
| 6 | [05_Comprobar_Simulacion.sql](../01_Base_Datos/05_Comprobar_Simulacion.sql) | Consulta cantidades, bitácora, duplicados e indicadores. |

### 6.1 Paso 1: crear y poblar el OLTP

1. Abre `01_Base_Datos/01_Estructura_y_Datos.sql` en SSMS.
2. Ejecuta todo el archivo.
3. En Mensajes, comprueba que no haya errores.
4. En Resultados debes obtener el resumen de asistencias por mes: julio 203, agosto 186 y septiembre 193.
5. En el Explorador, pulsa con el botón derecho sobre **Databases** y selecciona **Refresh / Actualizar**. Debe aparecer `A&SG_OLTP`.

Este archivo genera diez trabajadores, 582 asistencias y 582 tareas. Siete trabajadores tienen jornadas de lunes a viernes y tres practicantes de lunes, miércoles y viernes. Son movimientos simulados para validar el proyecto.

El generador verifica registros existentes, pero no se utiliza como migración de cualquier base ajena. Si avisa que un identificador pertenece a otra persona o proyecto, no cambies identificadores al azar ni borres datos: revisa la versión y el padrón.

### 6.2 Paso 2: crear el Data Mart

1. Abre `01_Base_Datos/02_Creacion_Data_Mart.sql`.
2. Ejecútalo una sola vez si esa base todavía no existe.
3. Actualiza la lista de bases del Explorador.
4. Expande `A&SG_DataMart → Tables / Tablas`.
5. Debes encontrar `dim_trabajador`, `dim_tiempo`, `dim_proyecto`, `dim_administrador`, `fac_rendimiento_kpis`, `bitacora_etl` y `rechazos_etl`.

En este momento **la tabla de hechos está vacía**. Es el resultado esperado de crear únicamente la estructura. No insertes filas manualmente en ella.

### 6.3 Paso 3: instalar el procedimiento ETL

1. Abre `02_Procedimientos_Almacenados/02_Procedimiento_ETL.sql`.
2. Ejecútalo completo.
3. En el Explorador, expande `A&SG_DataMart → Programmability / Programación → Stored Procedures / Procedimientos almacenados`.
4. Actualiza la carpeta si hace falta y busca `dbo.usp_cargar_rendimiento`.

El procedimiento ya está definido, pero todavía no se ejecutó. **`CREATE OR ALTER PROCEDURE` no carga datos por sí solo.**

### 6.4 Paso 4: crear las vistas

1. Abre `02_Procedimientos_Almacenados/03_Vistas_PowerBI.sql`.
2. Ejecútalo completo.
3. Expande `A&SG_DataMart → Views / Vistas` y actualiza la carpeta.
4. Comprueba que aparezcan las cinco vistas del modelo: `vw_dim_trabajador`, `vw_dim_tiempo`, `vw_dim_proyecto`, `vw_dim_administrador` y `vw_rendimiento_kpis`.
5. También se crean `vw_indicadores_mensuales` y `vw_calidad_cargas`, útiles para comprobar los resultados.

### 6.5 Paso 5: ejecutar la carga

1. Abre `01_Base_Datos/04_Cargar_Simulacion.sql`.
2. Ejecuta el archivo completo.
3. El cargador comprobará que estén instalados sus componentes y que existan asistencias y tareas en el trimestre.
4. En los resultados busca la ejecución con estado **Completada** y cero rechazos.
5. La consulta final debe mostrar `1164` filas de hechos, `582` asistencias y `582` tareas.

El procedimiento lee el OLTP, limpia textos, valida referencias y fechas, actualiza dimensiones y reemplaza los hechos del intervalo dentro de una transacción. Las incidencias quedan registradas. Ejecuta una carga a la vez, sin otra transacción abierta y sin modificar el origen mientras se demuestra el proceso.

Si los componentes ya están instalados, la invocación equivalente es:

```sql
USE [A&SG_DataMart];
GO
EXEC dbo.usp_cargar_rendimiento '20260701', '20260930';
GO
```

Este comando no instala componentes: necesita los pasos anteriores.

### 6.6 Paso 6: comprobar la simulación

1. Abre `01_Base_Datos/05_Comprobar_Simulacion.sql`.
2. Ejecútalo completo.
3. Revisa sus conjuntos de resultados según el apartado siguiente.

Este archivo consulta los datos; no vuelve a cargar el trimestre. Si falta una vista, regresa al paso 4. Si no hay cargas registradas, regresa al paso 5.

### 6.7 Archivo 03 de la carpeta Base de Datos

[03_Alinear_Personal_Origen.sql](../01_Base_Datos/03_Alinear_Personal_Origen.sql) corrige el padrón de una instalación antigua. No es un paso obligatorio entre la creación y la carga de una instalación nueva. Utilízalo solo en el caso descrito en [08_Padron_Trabajadores.md](08_Padron_Trabajadores.md), con la copia de seguridad que corresponda.

<a id="comprobacion"></a>
## 7. Comprobar cantidades e indicadores

### 7.1 Resultados del conjunto inicial

| Control | Resultado esperado |
| --- | ---: |
| Trabajadores | 10 |
| Asistencias | 582 |
| Tareas | 582 |
| Filas de hechos | 1.164 |
| Resúmenes trabajador-mes | 30 |
| Última carga | Completada |
| Rechazos de esa carga | 0 |
| Grupos duplicados de claves | 0 |

| Mes de 2026 | Asistencias | Tareas |
| --- | ---: | ---: |
| Julio | 203 | 203 |
| Agosto | 186 | 186 |
| Septiembre | 193 | 193 |
| Total | 582 | 582 |

Estas cantidades describen el conjunto simulado inicial. Si agregaste movimientos o modificaste estados, primero concilia con tu origen actual. No fuerces los datos para que coincidan con una captura antigua.

### 7.2 Consultar las cantidades manualmente

Abre una consulta nueva, copia y ejecuta:

```sql
USE [A&SG_DataMart];
GO
SELECT COUNT(*) AS filas_hechos,
       SUM(total_asistencias) AS asistencias,
       SUM(total_tareas) AS tareas
FROM dbo.fac_rendimiento_kpis;

SELECT TOP (5) id_carga, fecha_desde, fecha_hasta, estado,
       asistencias_extraidas, tareas_extraidas,
       registros_rechazados, filas_cargadas, mensaje
FROM dbo.bitacora_etl
ORDER BY id_carga DESC;
```

Las primeras filas de hechos pueden tener `total_tareas = 0`: representan asistencia. Las filas de tareas se guardan por separado. Esto evita multiplicar una marcación si hay tareas en varios proyectos. No son 1.164 empleados.

Los valores `id_rendimiento` e `id_carga` pueden empezar en números distintos y crecer después de repetir. No los uses para comparar si dos computadoras tienen las mismas medidas.

### 7.3 Consultar resultados por trabajador y mes

```sql
USE [A&SG_DataMart];
GO
SELECT nombre_completo, mes, total_asistencias, total_tareas,
       tpa, ict, tdt, iep
FROM dbo.vw_indicadores_mensuales
ORDER BY id_trabajador_origen, mes;
```

Deben aparecer treinta filas: tres meses por cada uno de los diez trabajadores. No son nombres duplicados de empleados.

### 7.4 Demostrar que repetir no acumula cantidades

1. Abre [01_Validacion_ETL.sql](01_Validacion_ETL.sql).
2. Ejecútalo completo, sin cambiar el origen entre sus dos cargas.
3. El script carga el trimestre, guarda sus claves y medidas, vuelve a cargar y compara en ambos sentidos con `EXCEPT`.
4. Debe mostrar **Las dos cargas conservan los mismos datos**.
5. La consulta de duplicados debe estar vacía. Vacía en este control significa que no encontró grupos duplicados; no que falten los hechos.

Este script sí ejecuta el ETL dos veces. Los pasos antiguos que lo utilizaban también cargaban el Data Mart; el archivo 04 hace explícita la carga para que no se omita.

### 7.5 Leer los indicadores

| Sigla | Significado y cálculo | Resultado global inicial |
| --- | --- | ---: |
| TPA | Tasa de puntualidad: a tiempo / asistencias × 100. Hasta 09:40:59 es a tiempo; desde 09:41:00 es tardanza. | 92,10% |
| ICT | Índice de cumplimiento: completadas sin observaciones / tareas × 100. Es una convención académica; no existe un campo de aprobación formal. | 56,36% |
| TDT | Tasa de devolución, según la definición del proyecto: tareas con `FUERA DE PLAZO` en observaciones / tareas × 100. No cuenta todas las correcciones. | 3,44% |
| IEP | Índice de efectividad ponderado: TPA × 0,30 + ICT × 0,50 + (100 − TDT) × 0,20. | 75,12 puntos |

La sigla es TPA. TPA e ICT se prefieren altos y TDT bajo. IEP es un puntaje sobre 100, no un sueldo. Para combinar meses se suman numeradores y denominadores; no se promedian directamente sus porcentajes. Si falta un denominador, la tasa queda vacía y no equivale a cero medido.

Los regulares tienen TPA de 100% por el generador. Benjamin tiene el mayor IEP del conjunto, pero su TPA es 95%; no es el mayor TPA. El diccionario completo está en [11_Indicadores_Dashboard.md](11_Indicadores_Dashboard.md).

<a id="estrella"></a>
## 8. Dibujar el modelo estrella en SSMS

Las relaciones físicas ya fueron creadas por el archivo 02. El diagrama sirve para verlas y capturarlas; no reemplaza crear las tablas.

1. En el Explorador, expande `A&SG_DataMart`.
2. Busca **Database Diagrams / Diagramas de base de datos**.
3. Si SSMS ofrece instalar los objetos de soporte de diagramas, acepta únicamente en tu base de desarrollo y con permisos para hacerlo.
4. Pulsa con el botón derecho sobre la carpeta y selecciona **New Database Diagram / Nuevo diagrama de base de datos**.
5. Agrega `dim_trabajador`, `dim_tiempo`, `dim_proyecto`, `dim_administrador` y `fac_rendimiento_kpis`.
6. Cierra la ventana de selección de tablas.
7. Coloca los hechos en el centro y las cuatro dimensiones alrededor. Las líneas de relación deben aparecer por las claves foráneas existentes.
8. Guarda el diagrama con un nombre reconocible, por ejemplo `Modelo_Estrella_Rendimiento`.
9. Ajusta el tamaño y toma una captura legible. No dibujes relaciones nuevas por nombre.

Si tu edición de SSMS no muestra el diseñador o tu cuenta no tiene permisos, puedes consultar las claves desde el Explorador y utilizar la [captura existente del modelo](Evidencias/03_Modelo_Estrella_SSMS.png). El ETL y Power BI no necesitan que el dibujo esté guardado para funcionar. Más detalle en [07_Modelo_Estrella_SSMS.md](07_Modelo_Estrella_SSMS.md).

<a id="reporte-existente"></a>
## 9. Abrir el reporte terminado en Power BI

Este recorrido es el más corto para comprobar la entrega y preparar la demostración. El archivo ya tiene las medidas y visuales; no necesitas crearlos otra vez.

### 9.1 Abrir y guardar una copia de trabajo

1. Abre Power BI Desktop.
2. Selecciona **Archivo → Abrir** y busca [Reporte_Rendimiento_Personal.pbix](../03_Vistas_PowerBI/Reporte_Rendimiento_Personal.pbix) en la carpeta descargada.
3. Si la aplicación indica que el archivo fue creado con una versión más reciente, actualiza Desktop desde su fuente oficial antes de continuar.
4. Guarda una copia con **Archivo → Guardar como**, por ejemplo `Simulacion_Rendimiento_Personal.pbix`, en tu carpeta de trabajo. No sobrescribas la única copia terminada antes de ensayar.

También existe `Bono_por_efectividad.pbix`. En la versión revisada contiene el mismo reporte de dos páginas; utiliza el nombre principal anterior para evitar confusiones.

### 9.2 Cambiar el origen de datos

1. Mantén SQL Server iniciado.
2. En Power BI, abre **Archivo → Opciones y configuración → Configuración de origen de datos**. Según la versión también puede aparecer desde el menú de **Transformar datos**.
3. Selecciona la conexión de SQL Server utilizada por el archivo actual.
4. Pulsa **Cambiar origen** cuando esté disponible.
5. Sustituye el servidor guardado por el de tu computadora, consultado en SSMS. Mantén `A&SG_DataMart` como base.
6. Acepta el cambio. Si el servidor también está definido en parámetros o consultas, revisa **Transformar datos → Configuración de origen de datos** y la conexión de esas consultas.
7. En **Editar permisos** o en el aviso que aparezca al conectar, configura la autenticación válida para esa instancia. Para Windows se utilizan los permisos de tu usuario; para autenticación de base de datos, el usuario SQL autorizado.
8. Pulsa **Actualizar** en Inicio y espera a que terminen los avisos.
9. Comprueba las páginas inferiores **Rendimiento del personal** y **Bono por efectividad**.

No copies el servidor de las capturas. No introduzcas un correo de GitHub como credencial de SQL Server. Cambiar el nombre del servidor no crea la base: la instalación de los apartados anteriores debe existir en esa instancia.

### 9.3 Comprobar lo que aparece

1. En la página de rendimiento, limpia los filtros de trabajador y mes.
2. Debes ver 582 asistencias, 582 tareas y las cuatro tasas/puntajes del apartado 7.5.
3. Selecciona septiembre y Edu Cruz; los valores de comprobación están en el apartado 12.5.
4. Limpia de nuevo los filtros.
5. En la página del bono, revisa los importes del apartado 13.
6. Guarda la copia local con **Ctrl + S**.

La tarjeta Total tareas puede estar alojada en `vw_dim_administrador` dentro del panel de campos del PBIX. Esa ubicación de la medida no cambia por sí sola su cálculo; busca el icono de calculadora. No cambies relaciones para mover una medida.

Si solo necesitas abrir el archivo terminado, puedes pasar al apartado 14. Para mostrar cómo se construye, añade una página vacía en tu copia y sigue el apartado 12 usando las medidas existentes.

<a id="reporte-nuevo"></a>
## 10. Construir el reporte desde una página vacía

Este recorrido explica la construcción completa. Es más largo que la demostración de diez minutos. No intentes configurar desde cero todas las medidas y relaciones durante ese tiempo si no lo has ensayado.

### 10.1 Conectar un archivo nuevo

1. En Power BI Desktop, abre un reporte nuevo con **Archivo → Nuevo**.
2. En Inicio, pulsa **Obtener datos → SQL Server**. Si no aparece, usa **Más** y busca SQL Server.
3. En **Servidor**, escribe la instancia utilizada en SSMS.
4. En **Base de datos**, escribe `A&SG_DataMart`.
5. Selecciona **DirectQuery**, que es el modo indicado para esta construcción del proyecto. Necesitará SQL Server disponible al consultar.
6. Acepta y configura las credenciales autorizadas.
7. En la ventana Navegador, selecciona únicamente estas cinco vistas:

| Seleccionar | No confundir con |
| --- | --- |
| `dbo.vw_dim_trabajador` | La tabla OLTP Trabajadores. |
| `dbo.vw_dim_tiempo` | Una tabla de fechas creada automáticamente. |
| `dbo.vw_dim_proyecto` | Proyectos del OLTP. |
| `dbo.vw_dim_administrador` | Administrador del OLTP. |
| `dbo.vw_rendimiento_kpis` | La vista mensual o una segunda copia de los hechos. |

8. Pulsa **Cargar**. No es necesario pegar consultas SQL en la ventana de conexión para este recorrido.
9. Cuando termine, comprueba que aparecen las cinco vistas en el panel **Datos**; algunas versiones lo llaman **Campos**.

### 10.2 Crear las cuatro relaciones

1. En la barra izquierda, selecciona la vista **Modelo**, identificada por un diagrama de tablas.
2. Si se crearon relaciones automáticamente, revísalas antes de agregar otras. No crees duplicados.
3. Abre **Administrar relaciones → Nueva**.
4. Selecciona la dimensión y el campo de su identificador; en el otro lado, la vista de hechos y el mismo campo.
5. Utiliza cardinalidad **Uno a varios (1:*)**, con el uno en la dimensión y varios en hechos. Si el diálogo presenta primero hechos, se verá `*:1` con los lados invertidos; el significado debe ser el mismo.
6. Selecciona dirección de filtro **Única** desde dimensión hacia hechos.
7. Marca la relación como activa y acepta.
8. Repite hasta completar esta tabla:

| Dimensión: lado uno | Columna en ambos lados | Hechos: lado varios |
| --- | --- | --- |
| `vw_dim_trabajador` | `id_trabajador` | `vw_rendimiento_kpis` |
| `vw_dim_tiempo` | `id_tiempo` | `vw_rendimiento_kpis` |
| `vw_dim_proyecto` | `id_proyecto` | `vw_rendimiento_kpis` |
| `vw_dim_administrador` | `id_administrador` | `vw_rendimiento_kpis` |

9. Las relaciones deben aparecer activas, con cuatro líneas que conectan dimensiones y hechos.
10. No relaciones las dimensiones entre sí. No relaciones por `nombre_completo`, `mes` ni columnas terminadas en `_origen`.

Si Power BI propone muchos a muchos, detente y revisa las columnas elegidas y la unicidad de la dimensión. No aceptes esa cardinalidad para continuar rápidamente.

Puedes comparar con [06_Modelo_PowerBI.png](../03_Vistas_PowerBI/06_Modelo_PowerBI.png).

<a id="medidas"></a>
## 11. Crear las medidas y darles formato

Si abriste el PBIX terminado, sus medidas ya existen: no vuelvas a crearlas con los mismos nombres. Este apartado se utiliza al construir un archivo nuevo.

### 11.1 Crear una medida sin duplicar el signo igual

1. En el panel Datos, selecciona `vw_rendimiento_kpis` para alojar las medidas.
2. Pulsa **Modelado → Nueva medida**; en otras versiones aparece en Inicio o con el botón derecho sobre la tabla.
3. La barra de fórmula mostrará algo como `Medida =`.
4. Selecciona **todo** el contenido de la barra y reemplázalo por una sola definición de las que siguen.
5. Pulsa Enter o el botón de confirmar.
6. Comprueba que aparece el nombre de la medida con el icono de calculadora.
7. Repite con la siguiente. No pegues las nueve medidas juntas dentro de una sola definición.

El contenido debe empezar, por ejemplo, por `Total asistencias = SUM(...)`; no por `Medida = Total asistencias = SUM(...)`.

### 11.2 Medidas necesarias para la página de rendimiento

Crea las siguientes en el orden indicado. Las primeras cinco son cantidades auxiliares y las cuatro últimas calculan los KPI.

**1. Total asistencias**

```dax
Total asistencias = SUM(vw_rendimiento_kpis[total_asistencias])
```

**2. Llegadas a tiempo**

```dax
Llegadas a tiempo = SUM(vw_rendimiento_kpis[asistencias_a_tiempo])
```

**3. Total tareas**

```dax
Total tareas = SUM(vw_rendimiento_kpis[total_tareas])
```

**4. Tareas sin observaciones**

```dax
Tareas sin observaciones = SUM(vw_rendimiento_kpis[tareas_sin_observaciones])
```

**5. Tareas fuera de plazo**

```dax
Tareas fuera de plazo = SUM(vw_rendimiento_kpis[tareas_fuera_plazo])
```

**6. TPA**

```dax
TPA = DIVIDE([Llegadas a tiempo], [Total asistencias])
```

**7. ICT**

```dax
ICT = DIVIDE([Tareas sin observaciones], [Total tareas])
```

**8. TDT**

```dax
TDT = DIVIDE([Tareas fuera de plazo], [Total tareas])
```

**9. IEP**

```dax
IEP =
IF(
	ISBLANK([TPA]) || ISBLANK([ICT]) || ISBLANK([TDT]),
	BLANK(),
	100 * ([TPA] * 0.30 + [ICT] * 0.50 + (1 - [TDT]) * 0.20)
)
```

### 11.3 Formato de las medidas

Selecciona una medida en el panel Datos y busca **Herramientas de medida / Formato**, o sus propiedades de formato en la versión que uses:

| Medida | Formato |
| --- | --- |
| Total asistencias, Llegadas a tiempo, Total tareas, Tareas sin observaciones y Tareas fuera de plazo | Número entero; cero decimales. |
| TPA, ICT y TDT | Porcentaje; dos decimales. |
| IEP | Número decimal; dos decimales. **No porcentaje.** |

Las medidas DAX de TPA, ICT y TDT devuelven razones entre cero y uno y el formato las muestra como porcentaje. Las vistas SQL muestran tasas de cero a cien. El IEP ya se calcula en escala de cero a cien; aplicarle formato porcentual produciría un valor incorrecto de presentación.

Si una fórmula no se acepta, comprueba primero nombres de tablas/campos y que no dejaste `Medida =` delante. Las fórmulas del repositorio usan punto decimal y comas para separar argumentos. Si tu configuración usa separadores DAX localizados, revisa esa opción en la configuración regional de Power BI antes de cambiar las fórmulas al azar.

El archivo completo, con medidas adicionales, está en [Medidas_PowerBI.dax](Medidas_PowerBI.dax). Horas de permanencia y jornadas sin marca no equivalen por sí solas a horas pagables o faltas injustificadas.

<a id="rendimiento"></a>
## 12. Crear tarjetas, filtros y barras

Este apartado funciona tanto en un archivo nuevo con modelo y medidas completos como en una página nueva del PBIX terminado.

### 12.1 Preparar la página

1. Selecciona la vista **Informe**, identificada por el icono de gráfico en la barra izquierda.
2. Si necesitas una página nueva, pulsa **+** junto a las pestañas inferiores.
3. Pulsa con el botón derecho sobre la pestaña y elige **Cambiar nombre**. Usa **Rendimiento del personal** en un archivo nuevo o **Simulación en clase** en la copia para demostrar.
4. En **Insertar → Cuadro de texto**, escribe `A&SG S.A.C. · Julio–septiembre de 2026`.
5. Colócalo en la parte superior. Un tamaño de página panorámico 16:9 facilita ordenar el contenido, pero no cambia los cálculos.
6. Si no aparecen los paneles Datos o Visualizaciones, búscalos en **Ver → Paneles**. Las versiones recientes pueden presentar **Compilar visual** o edición sobre el objeto.

### 12.2 Crear la primera tarjeta y las otras cinco

1. Haz clic en un espacio vacío de la página.
2. En Visualizaciones, selecciona **Tarjeta**. El icono puede cambiar entre la tarjeta clásica y la nueva; ambas pueden mostrar una medida.
3. Busca **Total asistencias** en Datos. Arrastra la medida con icono de calculadora al área **Datos / Valores** de la tarjeta.
4. Debe mostrar **582** sin filtros. Si no es así, revisa la carga y filtros antes de continuar.
5. Selecciona la tarjeta y usa el panel **Formato visual** para ajustar tamaño de número, etiqueta, fondo y borde.
6. Mueve y ajusta la tarjeta con sus controles de esquina.
7. Para duplicarla, selecciónala, pulsa **Ctrl + C** y **Ctrl + V**.
8. En la tarjeta duplicada, retira la medida anterior del área Datos/Valores y agrega la siguiente.
9. Repite hasta tener estas seis tarjetas:

| Tarjeta | Valor global inicial |
| --- | ---: |
| Total asistencias | 582 |
| Total tareas | 582 |
| TPA | 92,10% |
| ICT | 56,36% |
| TDT | 3,44% |
| IEP | 75,12 |

10. Distribúyelas en dos filas de tres. Mantén tamaños y alineación consistentes. No es necesario reproducir exactamente el borde de la captura.

Elige las medidas por su nombre, no la suma automática de una columna distinta. Si una tarjeta muestra 582 en lugar de un porcentaje, comprueba qué campo arrastraste.

### 12.3 Crear los dos segmentadores o filtros visibles

**Filtro de mes:**

1. Haz clic en un espacio vacío y elige **Segmentación de datos**.
2. Arrastra `vw_dim_tiempo[nombre_mes]` al campo del segmentador.
3. En Formato, elige una lista si deseas ver casillas, o un desplegable si necesitas ahorrar espacio.
4. Pon el título **Mes de análisis**. En muchas versiones está en **General → Título**.
5. Si debajo aparece `nombre_mes` y no lo quieres mostrar, desactiva **Encabezado de segmentación / Encabezado del segmentador**. El título personalizado puede seguir visible.
6. Para ordenar los nombres cronológicamente, selecciona la columna `nombre_mes` y utiliza **Herramientas de columna → Ordenar por columna → mes**, cuando esté disponible en tu modo de conexión. Después ordena el segmentador en forma ascendente. Si tu versión no permite configurar ese orden en DirectQuery, puedes usar el número `mes` en el segmentador o mantener los nombres, dejando claro el período; no cambies los valores del origen por una cuestión visual.

**Filtro de trabajador:**

1. Inserta otro segmentador.
2. Arrastra `vw_dim_trabajador[nombre_completo]`.
3. Elige estilo desplegable.
4. Pon el título **Trabajador** y oculta el encabezado técnico si lo deseas.

**Uso:** pulsa una casilla o elige un nombre para filtrar. Según la configuración del segmentador, varias selecciones pueden requerir Ctrl. Para borrar una selección, utiliza el icono de borrador o elimina las selecciones activas. No confundas dejar todos los valores disponibles con seleccionar únicamente **(En blanco)**.

Si aparece **(En blanco)**, consulta el diagnóstico del apartado 16. No representa un cuarto mes y no debe ocultarse para sustituir una comprobación de datos.

### 12.4 Crear el gráfico de barras

1. Haz clic en una zona vacía.
2. Selecciona **Gráfico de barras agrupadas**: barras horizontales.
3. Arrastra `vw_dim_trabajador[nombre_completo]` al **Eje Y**.
4. Arrastra la medida `[IEP]` al **Eje X / Valores**, según la interfaz.
5. En los tres puntos del visual, selecciona **Ordenar por IEP → Descendente**.
6. En Formato → General → Título, escribe **Efectividad por trabajador**.
7. En los ajustes del eje Y, desactiva su título si aparece `nombre_completo`. Conserva los nombres de las personas como categorías.
8. Puedes activar etiquetas de datos para mostrar los puntajes. Ensancha el visual si los nombres se cortan.
9. Sin selección de trabajador deben aparecer diez barras. Si solo aparece una después de filtrar a una persona, es el comportamiento esperado.

En esta página no añadas un filtro de proyecto o administrador para interpretar TPA o IEP: el origen no asigna la asistencia a esos elementos. Sus claves cero evitan inventar esa relación. Los análisis de proyectos pueden utilizar métricas de tareas, fuera de este recorrido principal.

### 12.5 Probar un caso individual

1. En mes, selecciona **Septiembre**.
2. En trabajador, selecciona **Edu Cruz**.
3. Debes obtener:

| Medida | Valor |
| --- | ---: |
| Total asistencias | 22 |
| Total tareas | 22 |
| TPA | 100,00% |
| ICT | 59,09% |
| TDT | 0,00% |
| IEP | 79,55 |

4. Explica que el mismo reporte cambió por el contexto de filtros.
5. Borra ambos filtros. Comprueba que regresan los valores globales.
6. Si hiciste clic en una barra y el resto quedó resaltado o filtrado, pulsa una zona vacía del gráfico para quitar esa selección.
7. Guarda el archivo con **Ctrl + S**.

La captura publicada de referencia está en [Reporte por rendimiento.png](../03_Vistas_PowerBI/Reporte%20por%20rendimiento.png).

<a id="bono"></a>
## 13. Crear la página del bono referencial

Si abriste el PBIX terminado, esta página ya existe. Revisa los resultados sin volver a crear medidas ni duplicar tablas. Para construirla desde cero, sigue estos pasos.

### 13.1 Entender los supuestos

- Base mensual referencial: **S/ 1.500**.
- Bono máximo: **20%**, equivalente a S/ 300.
- Se utiliza el IEP del trimestre seleccionado para ilustrar un bono de un mes.
- Bono = base × 20% × IEP / 100.
- Total referencial = base + bono.

El ejemplo no calcula tres sueldos, descuentos, aportes, impuestos ni beneficios. Un puntaje bajo reduce el bono del ejemplo, no la base. Aplicar una base común permite explicar la fórmula; no establece equivalencia contractual entre jornadas.

### 13.2 Crear las cuatro medidas monetarias

Utiliza **Nueva medida**, una definición por vez, después de haber creado IEP:

```dax
Sueldo base referencial = 1500
```

```dax
Porcentaje maximo de bono = 0.20
```

```dax
Bono referencial =
IF(
	HASONEVALUE(vw_dim_trabajador[id_trabajador]) && NOT(ISBLANK([IEP])),
	ROUND([Sueldo base referencial] * [Porcentaje maximo de bono] * [IEP] / 100, 2),
	BLANK()
)
```

```dax
Remuneracion referencial =
IF(
	HASONEVALUE(vw_dim_trabajador[id_trabajador]) && NOT(ISBLANK([IEP])),
	[Sueldo base referencial] + [Bono referencial],
	BLANK()
)
```

Las medidas de bono y total quedan vacías si no hay un solo trabajador en el contexto o no puede calcularse IEP. No son un total de planilla.

Da formato de **porcentaje** a Porcentaje maximo de bono. Da formato de moneda en soles y dos decimales a Sueldo base referencial, Bono referencial y Remuneracion referencial. Si el símbolo no aparece entre los formatos ofrecidos, revisa la configuración monetaria o indica explícitamente **S/** en el título del visual.

Las definiciones completas están en [Remuneracion_Referencial.dax](Remuneracion_Referencial.dax).

### 13.3 Crear la página y el aviso

1. Pulsa **+** y renombra la página como **Bono por efectividad**.
2. Agrega un título **Bono referencial por efectividad**.
3. Debajo, inserta un cuadro de texto visible:

> Simulación académica: base mensual S/ 1.500 y bono máximo 20%, proporcional al IEP. No representa una planilla real.

4. Para el resultado de referencia utiliza todo el trimestre, sin seleccionar un trabajador individual ni un proyecto. Si copiaste segmentadores de otras páginas, revisa **Ver → Sincronizar segmentaciones** para que un filtro de trabajador de la primera página no limite sin querer esta comparación.
5. Si incluyes segmentadores de fecha, selecciona el trimestre completo para comprobar los valores siguientes.

### 13.4 Tabla de mayor efectividad

1. Inserta un visual **Tabla**, no una tarjeta.
2. Agrega, en este orden: `vw_dim_trabajador[nombre_completo]`, `[IEP]`, `[Sueldo base referencial]`, `[Bono referencial]` y `[Remuneracion referencial]`.
3. Con la tabla seleccionada, busca el panel **Filtros → Filtros de este objeto visual**.
4. Abre el filtro de `nombre_completo`.
5. Cambia el tipo a **Top N / N superiores**.
6. Selecciona **Superior**, escribe **1** y arrastra `[IEP]` a **Por valor**.
7. Pulsa **Aplicar filtro**. No basta con escribir el número.
8. Cambia el título a **Mayor efectividad del trimestre**.
9. Desactiva el total de la tabla en Formato para que no se interprete como una planilla agregada.
10. Si lo deseas, usa **Cambiar nombre para este objeto visual** para mostrar Trabajador, Base referencial, Bono y Total referencial como encabezados legibles.

### 13.5 Tabla de menor efectividad

1. Duplica la tabla anterior con Ctrl + C y Ctrl + V.
2. Abre el filtro Top N de la copia.
3. Cambia **Superior** por **Inferior**, mantén **1** y `[IEP]` por valor.
4. Pulsa **Aplicar filtro**.
5. Pon el título **Menor efectividad del trimestre**.
6. No selecciones los nombres manualmente: deben responder al puntaje.

Para el conjunto y trimestre iniciales, sin otros filtros:

| Caso | Trabajador | IEP | Base | Bono | Total referencial |
| --- | --- | ---: | ---: | ---: | ---: |
| Mayor IEP | Benjamin Alfonso | 96,00 | S/ 1.500,00 | S/ 288,00 | S/ 1.788,00 |
| Menor IEP | Israel Rodrigo Ochoa Mejia | 22,00 | S/ 1.500,00 | S/ 66,00 | S/ 1.566,00 |

Si cambias el mes o los datos, el resultado puede variar. Un empate podría mostrar más de una persona con el filtro Top N; no hay empate en los extremos del trimestre inicial.

Compara con [Bono por efectividad.png](../03_Vistas_PowerBI/Bono%20por%20efectividad.png). El detalle del supuesto salarial está en [10_Ejemplo_Remuneracion.md](10_Ejemplo_Remuneracion.md).

<a id="entrega"></a>
## 14. Guardar, documentar y subir evidencias

### 14.1 Guardar en la computadora

1. Usa **Archivo → Guardar como** para guardar tu copia PBIX.
2. Cierra y vuelve a abrir la copia antes de exponer, con SQL Server iniciado.
3. Comprueba que puedes actualizar, filtrar y regresar al trimestre.
4. Para entregar una versión nueva, coordina con el equipo cuál será el archivo principal. Conserva el nombre `Reporte_Rendimiento_Personal.pbix` en el repositorio cuando esa sea la versión acordada.
5. No publiques en Power BI Service solo para poder mostrarlo en Desktop: no es necesario para este alcance.

### 14.2 Capturar evidencias

Utiliza **Windows + Shift + S** u otra herramienta de captura. Guarda un PNG real del estado que acabas de comprobar. No fabriques imágenes ni escribas resultados esperados como sustituto de ejecutarlos.

Evidencias disponibles:

| Evidencia | Archivo existente |
| --- | --- |
| Modelo SQL | [03_Modelo_Estrella_SSMS.png](Evidencias/03_Modelo_Estrella_SSMS.png) |
| Cargas y conciliación | [05_Conciliacion_Idempotencia.png](Evidencias/05_Conciliacion_Idempotencia.png) |
| Relaciones de Power BI | [06_Modelo_PowerBI.png](../03_Vistas_PowerBI/06_Modelo_PowerBI.png) |
| Rendimiento | [Reporte por rendimiento.png](../03_Vistas_PowerBI/Reporte%20por%20rendimiento.png) |
| Bono | [Bono por efectividad.png](../03_Vistas_PowerBI/Bono%20por%20efectividad.png) |
| Salida SQL de la prueba de instalación | [Resultados_Carga_Simulacion.txt](Evidencias/Resultados_Carga_Simulacion.txt) |

Para una captura nueva, indica en la descripción del aporte la fecha, el período, la versión del código, la instancia/versión SQL utilizada y quién produjo o revisó la evidencia. No incluyas contraseñas o contactos innecesarios.

### 14.3 Subir un aporte desde el navegador, sin usar Git

Para consultar y descargar no necesitas cuenta. Para modificar necesitas iniciar sesión con una cuenta autorizada en el repositorio o utilizar un fork según los permisos disponibles.

1. Abre el repositorio e inicia sesión.
2. Si vas a proponer un cambio, abre el selector de rama que suele mostrar **main**.
3. Escribe un nombre como `feature/evidencia-dashboard` y elige crear la rama desde main, si tienes permiso. Si no aparece esa opción, pide al responsable del repositorio que te habilite el flujo de colaboración; no cambies la identidad de otro integrante.
4. En la rama nueva, abre la carpeta correspondiente: reportes en `03_Vistas_PowerBI`, evidencias nuevas en la carpeta acordada de documentación.
5. Pulsa **Add file → Upload files**.
6. Selecciona o arrastra los archivos de tu computadora.
7. Revisa los nombres y escribe un mensaje breve que describa el aporte real.
8. Pulsa **Commit changes** para registrar la subida en esa rama.
9. Abre **Pull requests → New pull request**.
10. Selecciona **base: main** y **compare: tu rama**.
11. Comprueba en **Files changed** que solo aparecen los archivos que querías cambiar.
12. Añade una descripción de qué cambió y cómo lo verificaste y crea el pull request.
13. Comparte su enlace con el equipo. El cambio estará en main después de que se revise e integre.

Un commit registra un cambio; un pull request propone integrarlo. El autor que sube un archivo y quien lo elaboró pueden ser personas distintas, por lo que los aportes deben documentarse con claridad.

### 14.4 Enlazar archivos desde el informe

1. En GitHub, abre el archivo ya publicado.
2. Pulsa **Y**, cuando el atajo esté disponible, para convertir la dirección en un enlace permanente al commit. También puedes abrir el archivo desde la vista de un commit concreto.
3. Copia la dirección y pégala como vínculo en el manifiesto del informe.
4. Indica el código de evidencia, descripción, versión y responsable.
5. Comprueba que abre desde otra pestaña. Para un PBIX, explica que se descarga y se abre en Desktop; no es un dashboard web.

Si una guía cambia, el enlace a un commit antiguo seguirá mostrando la guía antigua. Cuando el informe describe esta versión de la instalación, debe citar el commit o la rama que realmente incluya esta guía y los archivos 04 y 05. El informe archivado no se actualiza automáticamente al cambiar un Markdown.

<a id="demostracion"></a>
## 15. Realizar la demostración en diez minutos

El PPT tiene cinco minutos aparte. Esta tabla organiza **hasta diez minutos de demostración**, con herramientas ya instaladas y la conexión ensayada. Si no has practicado, reconstruir toda la solución desde cero en ese plazo puede excederlo.

### 15.1 Preparar antes de entrar a clase

- Completar los pasos de SQL y comprobar el conjunto inicial.
- Abrir SSMS con una consulta preparada para ejecutar el ETL y otra para verificar cantidades.
- Abrir la copia PBIX con sus medidas y relaciones ya listas.
- Confirmar que ambas aplicaciones usan la misma instancia.
- Conservar las dos páginas terminadas.
- Ensayar una página adicional llamada **Simulación en clase**, sin alterar la única copia terminada. Puedes dejarla vacía en tu copia de ensayo para crear los visuales durante la demostración.
- Comprobar que la pantalla se ve y los nombres se leen con el tamaño de proyección que se utilizará.

### 15.2 Recorrido cronometrado

| Minutos | Acción y resultado que se muestra |
| --- | --- |
| 0:00–1:00 | Mostrar A&SG_OLTP, A&SG_DataMart y las cuatro dimensiones con hechos. Explicar origen y destino. |
| 1:00–2:30 | Ejecutar `04_Cargar_Simulacion.sql`. Mostrar la carga Completada, cero rechazos y cantidades 1.164/582/582. |
| 2:30–3:30 | Actualizar Power BI y mostrar las cuatro relaciones. Volver a la vista Informe. |
| 3:30–6:30 | En una página nueva, crear tarjetas con medidas existentes, dos segmentadores y barras según el apartado 12. La rapidez depende del ensayo. |
| 6:30–8:00 | Seleccionar septiembre y Edu Cruz, comprobar el ejemplo y limpiar filtros. |
| 8:00–9:30 | Abrir la página de bono terminada y explicar base, porcentaje e importes referenciales. |
| 9:30–10:00 | Guardar y cerrar con las cantidades conciliadas y la repetición del período. |

Este recorrido demuestra **creación de visuales sobre un modelo preparado**. No se presenta como construcción completa de bases, relaciones y todas las medidas dentro de diez minutos. Si el tiempo del ensayo no alcanza para seis tarjetas, muestra la creación de una tarjeta, los filtros y las barras, y utiliza la página terminada para explicar el conjunto; coordina esa adaptación con lo solicitado por el docente.

### 15.3 Frases de apoyo

- Al cargar: «Crear las tablas no llena los hechos. Ahora ejecutamos el procedimiento que extrae, valida y carga el trimestre».
- Al comprobar: «Los hechos tienen 1.164 filas; sus medidas suman 582 asistencias y 582 tareas».
- Al filtrar: «El mes y el trabajador cambian el contexto de las mismas medidas».
- Al mostrar el bono: «Estos importes ilustran una regla académica. No calculamos una planilla real».

Si surge un error, utiliza el mensaje real y los controles para diagnosticarlo. No presentes una captura antigua como una ejecución en vivo que acaba de ocurrir.

<a id="errores"></a>
## 16. Resolver errores frecuentes

### 16.1 SQL Server y archivos SQL

| Mensaje o síntoma | Causa que debes revisar | Cómo continuar |
| --- | --- | --- |
| No aparece ningún servidor o no conecta. | Motor no instalado, servicio detenido o nombre de instancia incorrecto. | Revisar el apartado 2.3 y el nombre del instalador. SSMS por sí solo no es el servidor. |
| Error de inicio de sesión. | Método de autenticación o usuario sin acceso. | Utilizar la cuenta autorizada y el método configurado; no inventar usuario/contraseña. |
| Certificado no confiable al conectar localmente con SSMS. | El servidor de desarrollo utiliza un certificado que el cliente no reconoce. | Verificar que sea tu instancia local. Revisar las opciones de conexión y, si corresponde a ese entorno de desarrollo, la opción Confiar en el certificado del servidor. No desactivar protecciones globales como solución general. |
| La base ya existe / objeto ya existe al ejecutar el DDL. | Se repitió el paso 2. | Detener ese archivo. Si el esquema ya es el vigente, continuar con procedimiento, vistas y carga. |
| No se encuentra A&SG_OLTP. | Paso 1 no terminó o se ejecutó en otra instancia. | Revisar el primer error del generador y el servidor de la pestaña. |
| No se encuentra A&SG_DataMart. | Falta paso 2 o conexión equivocada. | Crear en una instalación nueva o conectarse a la instancia correcta. |
| No se encuentra dbo.usp_cargar_rendimiento. | No se instaló el procedimiento. | Ejecutar completo el archivo del paso 3, después cargar. |
| No se encuentra una vista vw_. | No se ejecutó el paso 4 o el nombre no coincide. | Ejecutar el archivo de vistas y actualizar el Explorador. |
| La tabla fac_rendimiento_kpis devuelve cero filas. | Se creó la estructura pero no se ejecutó el ETL. | Ejecutar el paso 5 y revisar la bitácora. |
| El cargador dice que no hay asistencias o tareas del trimestre. | Origen sin datos de esas fechas o instancia incorrecta. | Revisar el paso 1 y sus mensajes; no insertar hechos manualmente. |
| La bitácora indica Fallida. | Error durante el proceso. | Leer `mensaje`, resolver el primer problema y volver a cargar. |
| La bitácora indica Con rechazos. | Registros que no cumplen las reglas. | Consultar rechazos; no asumir que el destino contiene todo el origen. |
| Solo parece ejecutarse una línea del archivo. | Había texto seleccionado al pulsar F5. | Quitar la selección y ejecutar el archivo adecuado completo; no repetir el DDL existente. |
| Las primeras filas tienen tareas en cero. | Son filas de asistencia. | Consultar SUM(total_tareas) o la vista mensual. |
| Los ID ya no empiezan en uno. | Hubo cargas anteriores y se regeneraron filas técnicas. | Comparar medidas y claves de negocio; no borrar para reiniciar el contador. |
| Error por identificadores de empleados ocupados. | Base de otra versión o datos incompatibles con el padrón. | Seguir la guía del padrón y pedir revisión de esa instalación. No borrar nombres o claves al azar. |

Para identificar dónde estás conectado:

```sql
SELECT @@SERVERNAME AS servidor, DB_NAME() AS base_actual;
```

Para leer incidencias después de una carga:

```sql
USE [A&SG_DataMart];
GO
SELECT TOP (5) * FROM dbo.bitacora_etl ORDER BY id_carga DESC;
SELECT * FROM dbo.rechazos_etl ORDER BY id_rechazo;
```

### 16.2 Power BI

| Síntoma | Qué revisar y hacer |
| --- | --- |
| El PBIX no abre. | Comprobar que se descargó completo como PBIX, no como HTML o texto. Revisar si pide una versión de Desktop más reciente. |
| El reporte pide el servidor de otro equipo. | Cambiar el origen siguiendo 9.2, introducir las credenciales correctas y actualizar. |
| SQL tiene datos, pero las tarjetas están vacías. | Revisar servidor, base, credenciales, carga y filtros de visual/página/reporte. Limpiar una selección de (En blanco) o un trabajador sin datos. |
| Las tarjetas repiten el mismo valor para todos los trabajadores. | Revisar la relación por id_trabajador y que el nombre del visual provenga de vw_dim_trabajador. |
| El gráfico de barras no muestra nada. | Confirmar nombre en eje Y, medida IEP en eje X y filtros válidos. Revisar si las tarjetas también quedaron vacías. |
| Error «la sintaxis de asistencias no es correcta». | Verificar que la fórmula sea `Total asistencias = SUM(...)`, sin `Medida =` delante. |
| Error de separadores o de nombre de campo. | Copiar una medida por vez y utilizar las cinco vistas exactas. Revisar configuración regional de DAX si usa separadores localizados. |
| IEP aparece como 7.512%. | Cambiar formato de IEP a número decimal. El valor ya está en escala de 0 a 100. |
| TPA aparece como 0,921 en vez de 92,10%. | Dar formato de porcentaje, dos decimales. No multiplicar de nuevo si utilizas la medida DAX de esta guía. |
| Los meses aparecen en orden alfabético. | Ordenar nombre_mes por mes, si lo permite el modelo, y después el visual en forma ascendente; alternativa: segmentar con el número de mes. |
| El bono muestra todos los trabajadores. | Revisar Top N superior/inferior 1, Por valor IEP y pulsar Aplicar filtro. |
| El bono queda vacío o no compara a todos. | Revisar selección individual de trabajador, filtros de página y segmentadores sincronizados. Las medidas necesitan un trabajador por fila e IEP válido. |
| Aparece una fila de total de sueldo o bono que confunde. | Desactivar el total de las dos tablas; las medidas no representan una planilla agregada. |
| «Muchos a muchos» al crear una relación. | Revisar que ambos campos sean el identificador interno correcto y que la dimensión sea única. No aceptar esa cardinalidad para este modelo. |

### 16.3 Valor (En blanco) en los meses

1. Comprueba que el segmentador use `vw_dim_tiempo[nombre_mes]`.
2. Comprueba que la relación activa sea por `id_tiempo` entre esa dimensión y los hechos.
3. Actualiza el reporte y revisa el origen al que se conecta.
4. En SQL puedes comprobar estas dos situaciones:

```sql
USE [A&SG_DataMart];
GO
SELECT * FROM dbo.dim_tiempo
WHERE fecha IS NULL OR nombre_mes IS NULL;

SELECT f.id_tiempo
FROM dbo.fac_rendimiento_kpis f
LEFT JOIN dbo.dim_tiempo d ON d.id_tiempo = f.id_tiempo
WHERE d.id_tiempo IS NULL;
```

En el modelo inicial con sus restricciones vigentes, esas consultas no deben mostrar filas. Si muestran datos, revisa esa instalación. Si SQL está correcto y Power BI conserva el valor vacío, vuelve a revisar modelo, filtros y conexión antes de excluirlo visualmente. No presentes el vacío como un mes adicional.

<a id="final"></a>
## 17. Lista final y límites de la simulación

Antes de dar por terminada la práctica, comprobar:

- [ ] SQL Server está iniciado y SSMS y Power BI usan la misma instancia.
- [ ] Se ejecutaron los seis pasos de instalación y carga que correspondan.
- [ ] El conjunto inicial muestra diez trabajadores, 582 asistencias, 582 tareas y 1.164 filas de hechos.
- [ ] La última carga está Completada y no tiene rechazos sin resolver.
- [ ] La comparación de dos cargas conserva las medidas y no aparecen grupos duplicados.
- [ ] Hay cuatro relaciones activas de uno a varios en Power BI.
- [ ] Las seis tarjetas sin filtros coinciden con el apartado 12.2.
- [ ] Septiembre y Edu Cruz coinciden con el ejemplo y después se limpiaron los filtros.
- [ ] Las tablas de bono muestran los dos casos del trimestre y el aviso de simulación.
- [ ] El PBIX se guardó y pudo volver a abrirse.
- [ ] Las capturas corresponden a la versión y al período declarados.
- [ ] Se ensayaron los cinco minutos de PPT y hasta diez de demostración, por separado.

Esta guía describe una solución académica de BI. No contiene una solución Big Data, extracción remota automática desde Clever Cloud, un cubo independiente de Analysis Services, cálculo legal de planillas ni actualización programada. La ausencia de una marca no demuestra una falta injustificada y el índice no mide toda la complejidad del trabajo. La revisión SQL no certifica que no existan vulnerabilidades ni demuestra mejoras de CPU o latencia.

La instalación y carga SQL tienen evidencia ejecutada en [Resultados_Carga_Simulacion.txt](Evidencias/Resultados_Carga_Simulacion.txt). La elaboración de esta guía se contrastó con los scripts, DAX y archivos existentes; no representa una nueva sesión de Power BI Desktop en vivo. Cada equipo debe realizar el ensayo local antes de la exposición.

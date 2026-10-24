# Guía completa de replicación y creación de dashboards

Esta guía comienza con la ejecución de los archivos SQL y continúa hasta guardar los reportes y presentar la simulación de julio–septiembre de 2026.

**Punto de partida:** repositorio descargado y extraído, SQL Server iniciado, SSMS conectado a la instancia de trabajo y Power BI Desktop instalado. En Power BI se utiliza **Importar** y el servidor **`.`** para la instancia local predeterminada. Para la primera instalación, utiliza una instancia donde todavía no existan las bases `A&SG_OLTP` y `A&SG_DataMart`. La creación del Data Mart se ejecuta una vez; las siguientes demostraciones repiten la carga y su comprobación.

Los nombres de archivo son enlaces: haz clic para abrirlos en GitHub o clic derecho → **Abrir enlace en una pestaña nueva** para conservar esta guía visible. Descarga cada SQL con **Download raw file**, ábrelo en SSMS con **Archivo → Abrir → Archivo** y ejecuta el archivo completo con **F5**, sin seleccionar una parte del código. Utiliza la misma instancia en SSMS y Power BI.

Hay dos recorridos para los dashboards:

| Opción | Qué vas a hacer | Apartados |
| --- | --- | --- |
| A: utilizar el reporte terminado | Descargar el PBIX de GitHub, abrirlo, conectar tu servidor y actualizar su copia de datos. | 4 y 9. |
| B: construir desde cero | Abrir un informe en blanco, importar las vistas, detectar y verificar relaciones, crear medidas, tarjetas, filtros, barras y las dos tablas del bono. | 5, 6, 7, 8 y 9, en orden. |

## Índice

1. [Crear las bases, instalar el ETL y cargar los datos](#instalacion)
2. [Comprobar cantidades e indicadores](#comprobacion)
3. [Dibujar el modelo estrella en SSMS](#estrella)
4. [Opción A: descargar y abrir el dashboard terminado](#reporte-existente)
5. [Opción B: crear los dashboards desde cero](#reporte-nuevo)
6. [Crear las medidas y darles formato](#medidas)
7. [Crear tarjetas, filtros y barras](#rendimiento)
8. [Crear la página del bono referencial](#bono)
9. [Guardar, documentar y subir evidencias](#entrega)
10. [Realizar la demostración en diez minutos](#demostracion)
11. [Lista final y límites de la simulación](#final)

<a id="instalacion"></a>
## 1. Crear las bases, instalar el ETL y cargar los datos

Mantén la misma instancia conectada durante todos los pasos. El número entre paréntesis es el orden de ejecución, no siempre el prefijo del archivo.

| Orden | Archivo que debes abrir | Qué debe ocurrir |
| --- | --- | --- |
| 1 | [01_Estructura_y_Datos.sql](../01_Base_Datos/01_Estructura_y_Datos.sql) | Crea y llena `A&SG_OLTP`. |
| 2 | [02_Creacion_Data_Mart.sql](../01_Base_Datos/02_Creacion_Data_Mart.sql) | Crea dimensiones, hechos y tablas de control. |
| 3 | [02_Procedimiento_ETL.sql](../02_Procedimientos_Almacenados/02_Procedimiento_ETL.sql) | Guarda la definición del procedimiento ETL. |
| 4 | [03_Vistas_PowerBI.sql](../02_Procedimientos_Almacenados/03_Vistas_PowerBI.sql) | Crea las vistas que consultará Power BI. |
| 5 | [04_Cargar_Simulacion.sql](../01_Base_Datos/04_Cargar_Simulacion.sql) | Ejecuta el ETL y llena el Data Mart. |
| 6 | [05_Comprobar_Simulacion.sql](../01_Base_Datos/05_Comprobar_Simulacion.sql) | Consulta cantidades, bitácora, duplicados e indicadores. |

### 1.1 Paso 1: crear y poblar el OLTP

1. Abre `01_Base_Datos/01_Estructura_y_Datos.sql` en SSMS.
2. Ejecuta todo el archivo.
3. En Mensajes, comprueba que no haya errores.
4. En Resultados debes obtener el resumen de asistencias por mes: julio 203, agosto 186 y septiembre 193.
5. En el Explorador, pulsa con el botón derecho sobre **Databases** y selecciona **Refresh / Actualizar**. Debe aparecer `A&SG_OLTP`.

Este archivo genera diez trabajadores, 582 asistencias y 582 tareas. Siete trabajadores tienen jornadas de lunes a viernes y tres practicantes de lunes, miércoles y viernes. Son movimientos simulados para validar el proyecto.

### 1.2 Paso 2: crear el Data Mart

1. Abre `01_Base_Datos/02_Creacion_Data_Mart.sql`.
2. Ejecútalo una sola vez si esa base todavía no existe.
3. Actualiza la lista de bases del Explorador.
4. Expande `A&SG_DataMart → Tables / Tablas`.
5. Debes encontrar `dim_trabajador`, `dim_tiempo`, `dim_proyecto`, `dim_administrador`, `fac_rendimiento_kpis`, `bitacora_etl` y `rechazos_etl`.

En este momento **la tabla de hechos está vacía**. Es el resultado esperado de crear únicamente la estructura. No insertes filas manualmente en ella.

### 1.3 Paso 3: instalar el procedimiento ETL

1. Abre `02_Procedimientos_Almacenados/02_Procedimiento_ETL.sql`.
2. Ejecútalo completo.
3. En el Explorador, expande `A&SG_DataMart → Programmability / Programación → Stored Procedures / Procedimientos almacenados`.
4. Actualiza la carpeta si hace falta y busca `dbo.usp_cargar_rendimiento`.

El procedimiento ya está definido, pero todavía no se ejecutó. **`CREATE OR ALTER PROCEDURE` no carga datos por sí solo.**

### 1.4 Paso 4: crear las vistas

1. Abre `02_Procedimientos_Almacenados/03_Vistas_PowerBI.sql`.
2. Ejecútalo completo.
3. Expande `A&SG_DataMart → Views / Vistas` y actualiza la carpeta.
4. Comprueba que aparezcan las cinco vistas del modelo: `vw_dim_trabajador`, `vw_dim_tiempo`, `vw_dim_proyecto`, `vw_dim_administrador` y `vw_rendimiento_kpis`.
5. También se crean `vw_indicadores_mensuales` y `vw_calidad_cargas`, útiles para comprobar los resultados.

### 1.5 Paso 5: ejecutar la carga

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

### 1.6 Paso 6: comprobar la simulación

1. Abre `01_Base_Datos/05_Comprobar_Simulacion.sql`.
2. Ejecútalo completo.
3. Revisa sus conjuntos de resultados según el apartado siguiente.

Este archivo consulta los datos y muestra los controles de la carga realizada.

<a id="comprobacion"></a>
## 2. Comprobar cantidades e indicadores

### 2.1 Resultados del conjunto inicial

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

Estas cantidades corresponden al conjunto simulado inicial de julio–septiembre de 2026.

### 2.2 Consultar las cantidades manualmente

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

### 2.3 Consultar resultados por trabajador y mes

```sql
USE [A&SG_DataMart];
GO
SELECT nombre_completo, mes, total_asistencias, total_tareas,
       tpa, ict, tdt, iep
FROM dbo.vw_indicadores_mensuales
ORDER BY id_trabajador_origen, mes;
```

Deben aparecer treinta filas: tres meses por cada uno de los diez trabajadores. No son nombres duplicados de empleados.

### 2.4 Demostrar que repetir no acumula cantidades

1. Abre [01_Validacion_ETL.sql](../04_Documentacion/01_Validacion_ETL.sql).
2. Ejecútalo completo, sin cambiar el origen entre sus dos cargas.
3. El script carga el trimestre, guarda sus claves y medidas, vuelve a cargar y compara en ambos sentidos con `EXCEPT`.
4. Debe mostrar **Las dos cargas conservan los mismos datos**.
5. La consulta de duplicados debe estar vacía. Vacía en este control significa que no encontró grupos duplicados; no que falten los hechos.

Este script sí ejecuta el ETL dos veces. Los pasos antiguos que lo utilizaban también cargaban el Data Mart; el archivo 04 hace explícita la carga para que no se omita.

### 2.5 Leer los indicadores

| Sigla | Significado y cálculo | Resultado global inicial |
| --- | --- | ---: |
| TPA | Tasa de puntualidad: a tiempo / asistencias × 100. Hasta 09:40:59 es a tiempo; desde 09:41:00 es tardanza. | 92,10% |
| ICT | Índice de cumplimiento: completadas sin observaciones / tareas × 100. Es una convención académica; no existe un campo de aprobación formal. | 56,36% |
| TDT | Tasa de devolución, según la definición del proyecto: tareas con `FUERA DE PLAZO` en observaciones / tareas × 100. No cuenta todas las correcciones. | 3,44% |
| IEP | Índice de efectividad ponderado: TPA × 0,30 + ICT × 0,50 + (100 − TDT) × 0,20. | 75,12 puntos |

La sigla es TPA. TPA e ICT se prefieren altos y TDT bajo. IEP es un puntaje sobre 100, no un sueldo. Para combinar meses se suman numeradores y denominadores; no se promedian directamente sus porcentajes. Si falta un denominador, la tasa queda vacía y no equivale a cero medido.

Los regulares tienen TPA de 100% por el generador. Benjamin tiene el mayor IEP del conjunto, pero su TPA es 95%; no es el mayor TPA. El diccionario completo está en [11_Indicadores_Dashboard.md](../04_Documentacion/11_Indicadores_Dashboard.md).

<a id="estrella"></a>
## 3. Dibujar el modelo estrella en SSMS

Las relaciones físicas ya fueron creadas por el archivo 02. El diagrama sirve para verlas y capturarlas; no reemplaza crear las tablas.

1. En el Explorador, expande `A&SG_DataMart`.
2. Busca **Database Diagrams / Diagramas de base de datos**.
3. Al abrir por primera vez los diagramas, acepta la creación de sus objetos de soporte en la base de desarrollo con tu cuenta autorizada.
4. Pulsa con el botón derecho sobre la carpeta y selecciona **New Database Diagram / Nuevo diagrama de base de datos**.
5. Agrega `dim_trabajador`, `dim_tiempo`, `dim_proyecto`, `dim_administrador` y `fac_rendimiento_kpis`.
6. Cierra la ventana de selección de tablas.
7. Coloca los hechos en el centro y las cuatro dimensiones alrededor. Las líneas de relación deben aparecer por las claves foráneas existentes.
8. Guarda el diagrama con un nombre reconocible, por ejemplo `Modelo_Estrella_Rendimiento`.
9. Ajusta el tamaño y toma una captura legible. No dibujes relaciones nuevas por nombre.

<a id="reporte-existente"></a>
## 4. Opción A: descargar y abrir el dashboard terminado

Este recorrido es el más corto para comprobar la entrega y preparar la demostración. El archivo ya tiene las medidas y visuales; no necesitas crearlos otra vez.

### 4.1 Descargar, abrir y guardar una copia de trabajo

1. Abre [Reporte_Rendimiento_Personal.pbix en GitHub](../03_Vistas_PowerBI/Reporte_Rendimiento_Personal.pbix). Puedes usar clic derecho → **Abrir enlace en una pestaña nueva** para mantener esta guía visible.
2. Pulsa **Download raw file / Descargar archivo sin procesar** y guarda el archivo con extensión `.pbix` en tu computadora.
3. Abre **Power BI Desktop** desde el menú Inicio de Windows.
4. Selecciona **Archivo → Abrir → Examinar** y abre el PBIX descargado. Abrir el PBIX recupera las páginas, medidas, modelo y visuales guardados; no es la opción Obtener datos.
5. Guarda una copia con **Archivo → Guardar como**, por ejemplo `Simulacion_Rendimiento_Personal.pbix`, en tu carpeta de trabajo.

También existe `Bono_por_efectividad.pbix`. En la versión revisada contiene el mismo reporte de dos páginas; utiliza el nombre principal anterior para evitar confusiones.

### 4.2 Cambiar el origen de datos

1. Mantén SQL Server iniciado.
2. En Power BI, abre **Archivo → Opciones y configuración → Configuración de origen de datos**. Según la versión también puede aparecer desde el menú de **Transformar datos**.
3. Selecciona la conexión de SQL Server utilizada por el archivo actual.
4. Pulsa **Cambiar origen** cuando esté disponible.
5. En **Servidor**, escribe `.` —un punto— para la instancia local predeterminada. En **Base de datos**, escribe `A&SG_DataMart`. Utiliza el mismo servidor en SSMS.
6. Acepta el cambio y comprueba el servidor y la base en la conexión de las consultas de **Transformar datos**.
7. En **Editar permisos** o en el aviso que aparezca al conectar, configura la autenticación válida para esa instancia. Para Windows se utilizan los permisos de tu usuario; para autenticación de base de datos, el usuario SQL autorizado.
8. Pulsa **Actualizar** en Inicio y espera a que terminen los avisos.
9. Comprueba las páginas inferiores **Rendimiento del personal** y **Bono por efectividad**.

El punto `.` identifica la instancia local predeterminada; no inicia el servicio SQL Server. En una instalación con nombre, utiliza `.\SQLEXPRESS` u otro nombre real de instancia, tanto en SSMS como en Power BI. La base debe estar cargada previamente según los apartados 1 y 2.

### 4.3 Utilizar Importar en la copia de trabajo

Abrir un PBIX conserva el modo de conexión con el que fue guardado. Cambiar el servidor no cambia automáticamente ese modo.

1. Selecciona la vista **Modelo** en la barra izquierda.
2. Selecciona una de las cinco tablas del modelo y abre el panel **Propiedades**.
3. Despliega **Avanzado** y consulta **Modo de almacenamiento**.
4. Para las tablas que ya indican **Importar**, conserva esa configuración. Para las que indican **DirectQuery**, selecciona **Importar** y confirma el cambio en tu copia local. La conversión a Importar es un cambio de una sola dirección para esas tablas.
5. Repite la revisión para `vw_dim_trabajador`, `vw_dim_tiempo`, `vw_dim_proyecto`, `vw_dim_administrador` y `vw_rendimiento_kpis`.
6. En **Inicio**, pulsa **Actualizar** con SQL Server iniciado para traer los datos a la copia del reporte.
7. Guarda con **Ctrl + S**. Conserva las relaciones, medidas y visuales del archivo.

En modo Importar, Power BI guarda una copia de los datos. Después de ejecutar otra carga ETL en SQL Server, pulsa **Actualizar** para incorporar sus resultados al reporte. Cambiar un filtro no vuelve a ejecutar el ETL.

### 4.4 Comprobar lo que aparece

1. En la página de rendimiento, limpia los filtros de trabajador y mes.
2. Debes ver 582 asistencias, 582 tareas y las cuatro tasas/puntajes del apartado 2.5.
3. Selecciona septiembre y Edu Cruz; los valores de comprobación están en el apartado 7.5.
4. Limpia de nuevo los filtros.
5. En la página del bono, revisa los importes del apartado 8.
6. Guarda la copia local con **Ctrl + S**.

La tarjeta Total tareas puede estar alojada en `vw_dim_administrador` dentro del panel de campos del PBIX. Esa ubicación de la medida no cambia por sí sola su cálculo; busca el icono de calculadora. No cambies relaciones para mover una medida.

Si solo necesitas abrir el archivo terminado, puedes pasar al apartado 9. Para mostrar cómo se construye, añade una página vacía en tu copia y sigue el apartado 7 usando las medidas existentes.

<a id="reporte-nuevo"></a>
## 5. Opción B: crear los dashboards desde cero

Este recorrido empieza en la primera apertura de Power BI Desktop y termina con las dos páginas del reporte. Después de completar la carga SQL de los apartados 1 y 2, sigue los apartados **5, 6, 7, 8 y 9**, en ese orden. No necesitas abrir un PBIX existente. La construcción completa se prepara antes de la demostración de diez minutos.

### 5.1 Conectar un archivo nuevo

Abre **Power BI Desktop** desde el menú Inicio de Windows. En la pantalla inicial elige **Informe en blanco**; también puedes entrar por **Archivo → Nuevo**. Trabajarás en Desktop con SQL Server local, sin publicar en Power BI Service.

Para este recorrido se utiliza la instancia local predeterminada de SQL Server, cuyo nombre abreviado es **`.`**. El servicio debe estar iniciado y `A&SG_DataMart` debe contener los resultados de la carga. En SSMS conéctate también a `.`. Si tu instalación es una instancia con nombre, usa su nombre real, por ejemplo `.\SQLEXPRESS`, en las dos aplicaciones.

Antes de cargar las vistas, activa la detección de relaciones:

1. Abre **Archivo → Opciones y configuración → Opciones**.
2. En **Archivo actual → Carga de datos**, busca **Relaciones**.
3. Activa **Detectar automáticamente nuevas relaciones después de cargar los datos**.
4. Mantén activada **Importar relaciones de orígenes de datos en la primera carga**, cuando aparezca esa opción.
5. Pulsa **Aceptar** para regresar al informe en blanco.

Ahora conecta el Data Mart:

1. Mantén abierto el informe en blanco.
2. En Inicio, pulsa **Obtener datos → SQL Server**. Si no aparece, usa **Más** y busca SQL Server.
3. En **Servidor**, escribe **`.`**, un punto sin comillas, para la instancia local predeterminada.
4. En **Base de datos**, escribe `A&SG_DataMart`.
5. En **Modo de conectividad de datos**, selecciona **Importar**. Power BI copiará los datos de las vistas al informe.
6. Pulsa **Aceptar**. En la ventana de credenciales selecciona **Windows → Usar mis credenciales actuales**, para la cuenta Windows autorizada en esa instancia, y pulsa **Conectar**. Una instancia configurada con usuario SQL utiliza la opción **Base de datos** y sus credenciales autorizadas.
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

### 5.2 Detectar automáticamente y comprobar el modelo estrella

1. Terminada la importación, pulsa el icono de **Modelo** en la barra izquierda: es el que muestra tablas conectadas.
2. Abre **Inicio / Modelado → Administrar relaciones** y pulsa **Detección automática / Autodetectar**. Power BI analiza las columnas importadas para proponer relaciones.
3. Cierra el cuadro y revisa las líneas del modelo. La configuración que debe quedar es la siguiente:

| Dimensión: lado uno | Columna en ambos lados | Hechos: lado varios |
| --- | --- | --- |
| `vw_dim_trabajador` | `id_trabajador` | `vw_rendimiento_kpis` |
| `vw_dim_tiempo` | `id_tiempo` | `vw_rendimiento_kpis` |
| `vw_dim_proyecto` | `id_proyecto` | `vw_rendimiento_kpis` |
| `vw_dim_administrador` | `id_administrador` | `vw_rendimiento_kpis` |

4. Abre cada relación con doble clic en su línea. Comprueba que utiliza el identificador de la tabla anterior, cardinalidad **Uno a varios (1:*)**, dirección de filtro **Única** desde dimensión hacia hechos y relación **Activa**. Pulsa **Aceptar** para guardar la configuración revisada.
5. Coloca `vw_rendimiento_kpis` en el centro arrastrando el encabezado de su tabla. Distribuye alrededor las cuatro dimensiones. La detección crea relaciones; la colocación visual se organiza con el ratón.
6. Guarda el archivo con **Archivo → Guardar como** y el nombre `Simulacion_Rendimiento_Personal.pbix` en tu carpeta de trabajo.
7. Continúa en el apartado 6 para crear las medidas; después completa los apartados 7, 8 y 9 para construir, comprobar y guardar las dos páginas finales.

La detección automática es una ayuda de Power BI y no garantiza las cuatro relaciones: el origen seleccionado contiene vistas, que no publican las claves foráneas como las tablas físicas. La tabla anterior define el modelo que se debe verificar. Para completar una relación no detectada, usa **Administrar relaciones → Nueva**, selecciona dimensión e identificador, hechos y el mismo identificador, y aplica **1:* → Única → Activa → Aceptar**. Conserva únicamente las cuatro relaciones indicadas, sin conexiones entre dimensiones.

Puedes comparar con [06_Modelo_PowerBI.png](../03_Vistas_PowerBI/06_Modelo_PowerBI.png).

<a id="medidas"></a>
## 6. Crear las medidas y darles formato

Si abriste el PBIX terminado, sus medidas ya existen: no vuelvas a crearlas con los mismos nombres. Este apartado se utiliza al construir un archivo nuevo.

### 6.1 Crear una medida

1. En el panel Datos, selecciona `vw_rendimiento_kpis` para alojar las medidas.
2. Pulsa **Modelado → Nueva medida**; en otras versiones aparece en Inicio o con el botón derecho sobre la tabla.
3. La barra de fórmula mostrará algo como `Medida =`.
4. Selecciona **todo** el contenido de la barra y reemplázalo por una sola definición de las que siguen.
5. Pulsa Enter o el botón de confirmar.
6. Comprueba que aparece el nombre de la medida con el icono de calculadora.
7. Repite con la siguiente. No pegues las nueve medidas juntas dentro de una sola definición.

Cada definición comienza con el nombre de la medida, seguido de un signo igual y su fórmula.

### 6.2 Medidas necesarias para la página de rendimiento

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

### 6.3 Formato de las medidas

Selecciona una medida en el panel Datos y busca **Herramientas de medida / Formato**, o sus propiedades de formato en la versión que uses:

| Medida | Formato |
| --- | --- |
| Total asistencias, Llegadas a tiempo, Total tareas, Tareas sin observaciones y Tareas fuera de plazo | Número entero; cero decimales. |
| TPA, ICT y TDT | Porcentaje; dos decimales. |
| IEP | Número decimal; dos decimales. **No porcentaje.** |

Las medidas DAX de TPA, ICT y TDT devuelven razones entre cero y uno y el formato las muestra como porcentaje. Las vistas SQL muestran tasas de cero a cien. El IEP ya se calcula en escala de cero a cien; aplicarle formato porcentual produciría un valor incorrecto de presentación.

El archivo completo, con medidas adicionales, está en [Medidas_PowerBI.dax](../04_Documentacion/Medidas_PowerBI.dax). Horas de permanencia y jornadas sin marca no equivalen por sí solas a horas pagables o faltas injustificadas.

<a id="rendimiento"></a>
## 7. Crear tarjetas, filtros y barras

Este apartado funciona tanto en un archivo nuevo con modelo y medidas completos como en una página nueva del PBIX terminado.

### 7.1 Preparar la página

1. Selecciona la vista **Informe**, identificada por el icono de gráfico en la barra izquierda.
2. Si necesitas una página nueva, pulsa **+** junto a las pestañas inferiores.
3. Pulsa con el botón derecho sobre la pestaña y elige **Cambiar nombre**. Usa **Rendimiento del personal** en un archivo nuevo o **Simulación en clase** en la copia para demostrar.
4. En **Insertar → Cuadro de texto**, escribe `A&SG S.A.C. · Julio–septiembre de 2026`.
5. Colócalo en la parte superior. Un tamaño de página panorámico 16:9 facilita ordenar el contenido, pero no cambia los cálculos.
6. Activa **Datos** y **Visualizaciones** desde **Ver → Paneles**. Las versiones recientes pueden presentar **Compilar visual** o edición sobre el objeto.

### 7.2 Crear la primera tarjeta y las otras cinco

1. Haz clic en un espacio vacío de la página.
2. En Visualizaciones, selecciona **Tarjeta**. El icono puede cambiar entre la tarjeta clásica y la nueva; ambas pueden mostrar una medida.
3. Busca **Total asistencias** en Datos. Arrastra la medida con icono de calculadora al área **Datos / Valores** de la tarjeta.
4. Sin filtros, la tarjeta muestra **582**.
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

Elige cada medida por su nombre e icono de calculadora para mostrar el indicador correspondiente.

### 7.3 Crear los dos segmentadores o filtros visibles

**Filtro de mes:**

1. Haz clic en un espacio vacío y elige **Segmentación de datos**.
2. Arrastra `vw_dim_tiempo[nombre_mes]` al campo del segmentador.
3. En Formato, elige una lista si deseas ver casillas, o un desplegable si necesitas ahorrar espacio.
4. Pon el título **Mes de análisis**. En muchas versiones está en **General → Título**.
5. Si debajo aparece `nombre_mes` y no lo quieres mostrar, desactiva **Encabezado de segmentación / Encabezado del segmentador**. El título personalizado puede seguir visible.
6. Para ordenar los nombres cronológicamente, selecciona la columna `nombre_mes` y utiliza **Herramientas de columna → Ordenar por columna → mes**. Después ordena el segmentador en forma ascendente.

**Filtro de trabajador:**

1. Inserta otro segmentador.
2. Arrastra `vw_dim_trabajador[nombre_completo]`.
3. Elige estilo desplegable.
4. Pon el título **Trabajador** y oculta el encabezado técnico si lo deseas.

**Uso:** pulsa una casilla o elige un nombre para filtrar. Según la configuración del segmentador, varias selecciones pueden requerir Ctrl. Para borrar una selección, utiliza el icono de borrador o elimina las selecciones activas. No confundas dejar todos los valores disponibles con seleccionar únicamente **(En blanco)**.

### 7.4 Crear el gráfico de barras

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

### 7.5 Probar un caso individual

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
6. Pulsa una zona vacía del gráfico para dejar sus barras sin selección.
7. Guarda el archivo con **Ctrl + S**.

La captura publicada de referencia está en [Reporte por rendimiento.png](../03_Vistas_PowerBI/Reporte%20por%20rendimiento.png).

<a id="bono"></a>
## 8. Crear la página del bono referencial

Si abriste el PBIX terminado, esta página ya existe. Revisa los resultados sin volver a crear medidas ni duplicar tablas. Para construirla desde cero, sigue estos pasos.

### 8.1 Entender los supuestos

- Base mensual referencial: **S/ 1.500**.
- Bono máximo: **20%**, equivalente a S/ 300.
- Se utiliza el IEP del trimestre seleccionado para ilustrar un bono de un mes.
- Bono = base × 20% × IEP / 100.
- Total referencial = base + bono.

El ejemplo no calcula tres sueldos, descuentos, aportes, impuestos ni beneficios. Un puntaje bajo reduce el bono del ejemplo, no la base. Aplicar una base común permite explicar la fórmula; no establece equivalencia contractual entre jornadas.

### 8.2 Crear las cuatro medidas monetarias

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

Da formato de **porcentaje** a Porcentaje maximo de bono. Da formato de moneda en soles y dos decimales a Sueldo base referencial, Bono referencial y Remuneracion referencial. Indica **S/** en los títulos de los importes.

Las definiciones completas están en [Remuneracion_Referencial.dax](../04_Documentacion/Remuneracion_Referencial.dax).

### 8.3 Crear la página y el aviso

1. Pulsa **+** y renombra la página como **Bono por efectividad**.
2. Agrega un título **Bono referencial por efectividad**.
3. Debajo, inserta un cuadro de texto visible:

> Simulación académica: base mensual S/ 1.500 y bono máximo 20%, proporcional al IEP. No representa una planilla real.

4. Para el resultado de referencia utiliza todo el trimestre, sin seleccionar un trabajador individual ni un proyecto. Mantén esta página independiente del segmentador de trabajador de la primera página en **Ver → Sincronizar segmentaciones**.
5. Utiliza el trimestre completo para comprobar los valores siguientes.

### 8.4 Tabla de mayor efectividad

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

### 8.5 Tabla de menor efectividad

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

Compara con [Bono por efectividad.png](../03_Vistas_PowerBI/Bono%20por%20efectividad.png). El detalle del supuesto salarial está en [10_Ejemplo_Remuneracion.md](../04_Documentacion/10_Ejemplo_Remuneracion.md).

<a id="entrega"></a>
## 9. Guardar, documentar y subir evidencias

### 9.1 Guardar en la computadora

1. Usa **Archivo → Guardar como** para guardar tu copia PBIX.
2. Cierra y vuelve a abrir la copia antes de exponer, con SQL Server iniciado.
3. Comprueba que puedes actualizar, filtrar y regresar al trimestre.
4. Para entregar una versión nueva, coordina con el equipo cuál será el archivo principal. Conserva el nombre `Reporte_Rendimiento_Personal.pbix` en el repositorio cuando esa sea la versión acordada.
5. No publiques en Power BI Service solo para poder mostrarlo en Desktop: no es necesario para este alcance.

### 9.2 Capturar evidencias

Utiliza **Windows + Shift + S** u otra herramienta de captura. Guarda un PNG real del estado que acabas de comprobar. No fabriques imágenes ni escribas resultados esperados como sustituto de ejecutarlos.

Evidencias disponibles:

| Evidencia | Archivo existente |
| --- | --- |
| Modelo SQL | [03_Modelo_Estrella_SSMS.png](../04_Documentacion/Evidencias/03_Modelo_Estrella_SSMS.png) |
| Cargas y conciliación | [05_Conciliacion_Idempotencia.png](../04_Documentacion/Evidencias/05_Conciliacion_Idempotencia.png) |
| Relaciones de Power BI | [06_Modelo_PowerBI.png](../03_Vistas_PowerBI/06_Modelo_PowerBI.png) |
| Rendimiento | [Reporte por rendimiento.png](../03_Vistas_PowerBI/Reporte%20por%20rendimiento.png) |
| Bono | [Bono por efectividad.png](../03_Vistas_PowerBI/Bono%20por%20efectividad.png) |
| Salida SQL de la prueba de instalación | [Resultados_Carga_Simulacion.txt](../04_Documentacion/Evidencias/Resultados_Carga_Simulacion.txt) |

Para una captura nueva, indica en la descripción del aporte la fecha, el período, la versión del código, la instancia/versión SQL utilizada y quién produjo o revisó la evidencia. No incluyas contraseñas o contactos innecesarios.

### 9.3 Subir un aporte desde el navegador, sin usar Git

Para consultar y descargar no necesitas cuenta. Para modificar necesitas iniciar sesión con una cuenta autorizada en el repositorio o utilizar un fork según los permisos disponibles.

1. Abre el repositorio e inicia sesión.
2. Si vas a proponer un cambio, abre el selector de rama que suele mostrar **main**.
3. Escribe `feature/evidencia-dashboard` y selecciona crear la rama desde **main** con tu cuenta autorizada.
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

### 9.4 Enlazar archivos desde el informe

1. En GitHub, abre el archivo ya publicado.
2. Pulsa **Y**, cuando el atajo esté disponible, para convertir la dirección en un enlace permanente al commit. También puedes abrir el archivo desde la vista de un commit concreto.
3. Copia la dirección y pégala como vínculo en el manifiesto del informe.
4. Indica el código de evidencia, descripción, versión y responsable.
5. Comprueba que abre desde otra pestaña. Para un PBIX, explica que se descarga y se abre en Desktop; no es un dashboard web.

Si una guía cambia, el enlace a un commit antiguo seguirá mostrando la guía antigua. Cuando el informe describe esta versión de la instalación, debe citar el commit o la rama que realmente incluya esta guía y los archivos 04 y 05. El informe archivado no se actualiza automáticamente al cambiar un Markdown.

<a id="demostracion"></a>
## 10. Realizar la demostración en diez minutos

El PPT tiene cinco minutos aparte. Esta tabla organiza **hasta diez minutos de demostración**, con herramientas instaladas, modelo y medidas preparados, y la conexión ensayada.

### 10.1 Preparar antes de entrar a clase

- Completar los pasos de SQL y comprobar el conjunto inicial.
- Abrir SSMS con una consulta preparada para ejecutar el ETL y otra para verificar cantidades.
- Abrir la copia PBIX con sus medidas y relaciones ya listas.
- Confirmar que ambas aplicaciones usan la misma instancia.
- Conservar las dos páginas terminadas.
- Ensayar una página adicional llamada **Simulación en clase**, sin alterar la única copia terminada. Puedes dejarla vacía en tu copia de ensayo para crear los visuales durante la demostración.
- Comprobar que la pantalla se ve y los nombres se leen con el tamaño de proyección que se utilizará.

### 10.2 Recorrido cronometrado

| Minutos | Acción y resultado que se muestra |
| --- | --- |
| 0:00–1:00 | Mostrar A&SG_OLTP, A&SG_DataMart y las cuatro dimensiones con hechos. Explicar origen y destino. |
| 1:00–2:30 | Ejecutar `04_Cargar_Simulacion.sql`. Mostrar la carga Completada, cero rechazos y cantidades 1.164/582/582. |
| 2:30–3:30 | Actualizar Power BI y mostrar las cuatro relaciones. Volver a la vista Informe. |
| 3:30–6:30 | En una página nueva, crear tarjetas con medidas existentes, dos segmentadores y barras según el apartado 7. La rapidez depende del ensayo. |
| 6:30–8:00 | Seleccionar septiembre y Edu Cruz, comprobar el ejemplo y limpiar filtros. |
| 8:00–9:30 | Abrir la página de bono terminada y explicar base, porcentaje e importes referenciales. |
| 9:30–10:00 | Guardar y cerrar con las cantidades conciliadas y la repetición del período. |

Este recorrido demuestra **creación de visuales sobre un modelo preparado**. La instalación de las bases, las relaciones y las medidas se completa antes de la exposición.

### 10.3 Frases de apoyo

- Al cargar: «Crear las tablas no llena los hechos. Ahora ejecutamos el procedimiento que extrae, valida y carga el trimestre».
- Al comprobar: «Los hechos tienen 1.164 filas; sus medidas suman 582 asistencias y 582 tareas».
- Al filtrar: «El mes y el trabajador cambian el contexto de las mismas medidas».
- Al mostrar el bono: «Estos importes ilustran una regla académica. No calculamos una planilla real».

<a id="final"></a>
## 11. Lista final y límites de la simulación

Antes de dar por terminada la práctica, comprobar:

- [ ] SQL Server está iniciado y SSMS y Power BI usan la misma instancia.
- [ ] Se ejecutaron los seis pasos de instalación y carga que correspondan.
- [ ] El conjunto inicial muestra diez trabajadores, 582 asistencias, 582 tareas y 1.164 filas de hechos.
- [ ] La última carga está Completada y no tiene rechazos sin resolver.
- [ ] La comparación de dos cargas conserva las medidas y no aparecen grupos duplicados.
- [ ] Hay cuatro relaciones activas de uno a varios en Power BI.
- [ ] Las seis tarjetas sin filtros coinciden con el apartado 7.2.
- [ ] Septiembre y Edu Cruz coinciden con el ejemplo y después se limpiaron los filtros.
- [ ] Las tablas de bono muestran los dos casos del trimestre y el aviso de simulación.
- [ ] El PBIX se guardó y pudo volver a abrirse.
- [ ] Las capturas corresponden a la versión y al período declarados.
- [ ] Se ensayaron los cinco minutos de PPT y hasta diez de demostración, por separado.

Esta guía describe una solución académica de BI. No contiene una solución Big Data, extracción remota automática desde Clever Cloud, un cubo independiente de Analysis Services, cálculo legal de planillas ni actualización programada. La ausencia de una marca no demuestra una falta injustificada y el índice no mide toda la complejidad del trabajo. La revisión SQL no certifica que no existan vulnerabilidades ni demuestra mejoras de CPU o latencia.

La instalación y carga SQL tienen evidencia ejecutada en [Resultados_Carga_Simulacion.txt](../04_Documentacion/Evidencias/Resultados_Carga_Simulacion.txt). La elaboración de esta guía se contrastó con los scripts, DAX y archivos existentes; no representa una nueva sesión de Power BI Desktop en vivo. Cada equipo debe realizar el ensayo local antes de la exposición.

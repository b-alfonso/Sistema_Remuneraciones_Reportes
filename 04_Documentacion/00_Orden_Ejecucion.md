# Orden de ejecución de la simulación

GitHub contiene scripts y reportes. Cada integrante debe ejecutar la instalación en su propio SQL Server; descargar el repositorio no copia una base ya cargada.

## Instalación desde cero

Abrir cada archivo completo en SSMS y ejecutarlo con **F5**, sin seleccionar solo unas líneas:

| Paso | Archivo | Resultado |
| --- | --- | --- |
| 1 | [01_Estructura_y_Datos.sql](../01_Base_Datos/01_Estructura_y_Datos.sql) | Crea y llena `A&SG_OLTP`: diez trabajadores, 582 asistencias y 582 tareas. |
| 2 | [02_Creacion_Data_Mart.sql](../01_Base_Datos/02_Creacion_Data_Mart.sql) | Crea las dimensiones y hechos **todavía vacíos**. Ejecutar una sola vez. |
| 3 | [02_Procedimiento_ETL.sql](../02_Procedimientos_Almacenados/02_Procedimiento_ETL.sql) | Instala `dbo.usp_cargar_rendimiento`; todavía no carga datos. |
| 4 | [03_Vistas_PowerBI.sql](../02_Procedimientos_Almacenados/03_Vistas_PowerBI.sql) | Crea las vistas de consulta. |
| 5 | [04_Cargar_Simulacion.sql](../01_Base_Datos/04_Cargar_Simulacion.sql) | **Ejecuta el ETL** y llena el Data Mart. |
| 6 | [05_Comprobar_Simulacion.sql](../01_Base_Datos/05_Comprobar_Simulacion.sql) | Muestra servidor, cantidades, bitácora, indicadores y duplicados. No modifica datos. |

El período inicial es julio–septiembre de 2026. No repetir la creación del Data Mart si ya existe; no borrar tablas para volver a cargar.

## Si ya ejecutaste los dos primeros archivos

Continuar desde el **paso 3**. Es normal que `SELECT * FROM dbo.fac_rendimiento_kpis` esté vacío antes del paso 5.

Si ya están instalados el procedimiento y las vistas, ejecutar únicamente los pasos **5 y 6**. Una carga a la vez, sin otra transacción abierta. El procedimiento reemplaza los hechos del intervalo dentro de una transacción; repetirlo no acumula las cantidades.

Para comprobar la repetición, ejecutar después [01_Validacion_ETL.sql](01_Validacion_ETL.sql): realiza dos cargas y compara sus medidas. No es un requisito adicional para que el paso 5 cargue los datos.

## Resultados esperados del conjunto inicial

| Mes de 2026 | Asistencias | Tareas |
| --- | ---: | ---: |
| Julio | 203 | 203 |
| Agosto | 186 | 186 |
| Septiembre | 193 | 193 |
| Total | 582 | 582 |

También deben aparecer diez trabajadores, treinta resúmenes mensuales, 1.164 filas de hechos, cero grupos duplicados y una última carga `Completada` con cero rechazos. Los identificadores de filas y cargas pueden variar entre computadoras.

Si aparece `Con rechazos`, revisar `rechazos_etl` antes de comparar con estas cantidades. Si el origen cambió, sus resultados pueden ser distintos del conjunto inicial.

## Instalaciones anteriores

[03_Alinear_Personal_Origen.sql](../01_Base_Datos/03_Alinear_Personal_Origen.sql) solo se utiliza para corregir el padrón de una instalación anterior. No hace falta en una instalación nueva con el generador vigente. Seguir [08_Padron_Trabajadores.md](08_Padron_Trabajadores.md) si los nombres todavía no coinciden.

Para abrir Power BI y resolver una tabla vacía, seguir la [guía unificada](09_Guia_Completa.md). El antiguo archivo 14 conserva un enlace hacia esa misma guía.

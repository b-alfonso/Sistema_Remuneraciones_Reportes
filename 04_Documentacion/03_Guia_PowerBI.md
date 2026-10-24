# Informe de Power BI

Para instrucciones paso a paso sin conocimientos previos, usar [09_Guia_Completa.md](09_Guia_Completa.md#reporte-existente). Este archivo conserva el resumen técnico de conexión y visuales.

La entrega usa [Reporte_Rendimiento_Personal.pbix](../03_Vistas_PowerBI/Reporte_Rendimiento_Personal.pbix), con dos páginas: rendimiento y bono. Para abrir ese archivo no es necesario crear otra vez sus medidas.

## Abrir en otra computadora

1. Crear las bases y ejecutar el ETL según [00_Orden_Ejecucion.md](00_Orden_Ejecucion.md).
2. Abrir el `.pbix` en Power BI Desktop.
3. En **Archivo → Opciones y configuración → Configuración de origen de datos**, cambiar el servidor si es diferente. La base es `A&SG_DataMart`.
4. Configurar las credenciales de esa instancia y actualizar los visuales. SQL Server debe estar disponible.

El nombre del servidor puede consultarse en SSMS:

```sql
SELECT SERVERPROPERTY('ServerName') AS servidor;
```

## Construir un informe nuevo

1. **Obtener datos → SQL Server**. Escribir servidor y base `A&SG_DataMart`.
2. Elegir **DirectQuery**, conectarse y cargar las cinco vistas de la tabla siguiente.
3. Crear cuatro relaciones activas, de uno a varios, con filtro único desde cada dimensión hacia los hechos.

| Dimensión | Columna en ambos lados | Tabla de hechos |
| --- | --- | --- |
| `vw_dim_trabajador` | `id_trabajador` | `vw_rendimiento_kpis` |
| `vw_dim_tiempo` | `id_tiempo` | `vw_rendimiento_kpis` |
| `vw_dim_proyecto` | `id_proyecto` | `vw_rendimiento_kpis` |
| `vw_dim_administrador` | `id_administrador` | `vw_rendimiento_kpis` |

No unir por nombres ni por columnas terminadas en `_origen`. No cargar también las tablas OLTP o la vista mensual como otra tabla de hechos.

## Medidas

Crear cada definición de [Medidas_PowerBI.dax](Medidas_PowerBI.dax) por separado con **Nueva medida**. Reemplazar todo el contenido inicial de la barra, incluido `Medida =`.

- TPA, ICT, TDT y tasas: porcentaje, dos decimales.
- IEP: decimal de 0 a 100; no formato de porcentaje.
- Cantidades: enteros.
- Sueldos y bonos referenciales: moneda en soles, dos decimales.

Las medidas del bono están en [Remuneracion_Referencial.dax](Remuneracion_Referencial.dax). Usar las medidas para calcular los totales; no promediar los porcentajes de varios meses.

## Página 1: Rendimiento del personal

- Tarjetas: Total asistencias, Total tareas, TPA, ICT, TDT e IEP.
- Segmentadores: `nombre_mes` y `nombre_completo`, de sus dimensiones.
- Barras horizontales: nombre del trabajador en el eje Y e IEP en el eje X. Ordenar por IEP descendente.
- Ordenar la columna `nombre_mes` por `mes` para mostrar julio, agosto y septiembre en secuencia.

No filtrar esta página por proyecto o administrador, porque el origen no asigna las asistencias a ellos. Si aparece `(En blanco)`, revisar la relación y los datos según [11_Indicadores_Dashboard.md](11_Indicadores_Dashboard.md).

## Página 2: Bono por efectividad

Agregar el aviso de simulación y dos tablas con trabajador, IEP, base, bono y total referencial. En la primera, usar el filtro visual **Top N superior 1 por IEP**; en la segunda, **inferior 1 por IEP**. No elegir los nombres manualmente.

La base de S/ 1.500 y el máximo de 20% son supuestos académicos. Los pasos y resultados están en [10_Ejemplo_Remuneracion.md](10_Ejemplo_Remuneracion.md).

## Comprobar y guardar

Sin filtros, deben verse 582 asistencias y 582 tareas. Para el trimestre, Benjamin tiene IEP 96 e Israel 22. Comparar los resultados por mes con `dbo.vw_indicadores_mensuales` en SSMS; esa vista usa tasas de 0 a 100 y DAX usa valores de 0 a 1 con formato porcentual.

Guardar en `03_Vistas_PowerBI/Reporte_Rendimiento_Personal.pbix`. Al modificarlo, subir la versión actualizada con el mismo nombre. Exportar un PDF es opcional; no hace falta publicar en Power BI Service para demostrarlo desde Desktop.

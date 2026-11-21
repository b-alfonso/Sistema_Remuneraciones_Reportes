-- Paso 1 de la guía · Exportar Asistencia y Tareas de A&SG_OLTP (solo IDs, sin nombres, correos, teléfonos ni PIN)
-- En SSMS: ejecutar cada consulta → clic derecho en la grilla de resultados → "Save Results As..." → CSV
-- (o Tasks → Export Data). Activar antes: Tools → Options → Query Results → Results to Grid →
-- "Include column headers when copying or saving the results".
-- Ajustar el nombre de las tablas si en A&SG_OLTP se llaman distinto.

USE [A&SG_OLTP];
GO

-- Asistencia.csv  (debe dar 582 filas)
SELECT ID_Asistencia, ID_Trabajador, Fecha_Entrada, Fecha_Salida, Fecha_Calculada, Estado_Asistencia
FROM dbo.Asistencia
ORDER BY ID_Asistencia;

-- Tareas.csv  (debe dar 582 filas)
SELECT ID_Tarea, ID_Trabajador, ID_Proyecto, Fecha, Fecha_Inicio, Fecha_Entrega, Estado_Tarea, Observaciones
FROM dbo.Tareas
ORDER BY ID_Tarea;

-- Control: conteos que deben coincidir con el informe (582 + 582)
SELECT (SELECT COUNT(*) FROM dbo.Asistencia) AS asistencias,
       (SELECT COUNT(*) FROM dbo.Tareas)     AS tareas;

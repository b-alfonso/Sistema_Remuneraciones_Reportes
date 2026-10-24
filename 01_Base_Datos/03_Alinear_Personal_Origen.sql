USE [A&SG_OLTP];
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
SET ANSI_WARNINGS ON;
SET ANSI_PADDING ON;
SET ARITHABORT ON;
SET CONCAT_NULL_YIELDS_NULL ON;
SET NUMERIC_ROUNDABORT OFF;
SET XACT_ABORT ON;
GO

DECLARE @personal TABLE (
	id_trabajador int PRIMARY KEY, id_empleado int, nombre nvarchar(150), cargo nvarchar(100), codigo nvarchar(20)
);


DECLARE @tabla_identidad sysname;
DECLARE @asistencias_antes int = (SELECT COUNT(*) FROM dbo.Asistencia);
DECLARE @tareas_antes int = (SELECT COUNT(*) FROM dbo.Tareas);

BEGIN TRY
	BEGIN TRANSACTION;

	IF EXISTS (SELECT 1 FROM dbo.Trabajadores WHERE ID_Trabajador = 4)
	BEGIN
		IF (SELECT COUNT(*) FROM dbo.Trabajadores) <> 10
			OR (SELECT COUNT(*) FROM dbo.Empleados) <> 11
			OR (SELECT COUNT(*) FROM dbo.Administrador) <> 1
			OR EXISTS (SELECT 1 FROM dbo.Empleados WHERE ID_Empleado NOT BETWEEN 1 AND 11)
			OR EXISTS (SELECT 1 FROM dbo.Trabajadores WHERE ID_Trabajador NOT IN (1,2,3,4,6,7,8,9,10,11))
			OR EXISTS (SELECT 1 FROM dbo.Trabajadores WHERE ID_Empleado <> ID_Trabajador
				OR Codigo_Trabajador <> N'TR-' + RIGHT(N'000' + CONVERT(nvarchar(3), ID_Trabajador), 3))
			OR NOT EXISTS (SELECT 1 FROM dbo.Administrador WHERE ID_Administrador = 1 AND ID_Empleado = 5)
			THROW 50500, N'El padrón no coincide con la instalación prevista. No se realizaron cambios.', 1;

		IF EXISTS (SELECT 1 FROM [A&SG_DataMart].dbo.dim_trabajador WHERE id_trabajador_origen = 5)
			THROW 50501, N'El Data Mart ya tiene un trabajador 5. Revise sus relaciones antes de continuar.', 1;

		SELECT CASE WHEN t.ID_Trabajador = 4 THEN 5 ELSE t.ID_Trabajador END AS id_trabajador,
			e.Correo, e.Telefono, e.Estado
		INTO #contactos
		FROM dbo.Trabajadores t JOIN dbo.Empleados e ON e.ID_Empleado = t.ID_Empleado;
		SELECT Correo, Telefono, Estado INTO #contacto_administrador FROM dbo.Empleados WHERE ID_Empleado = 5;

		SET IDENTITY_INSERT dbo.Empleados ON;
		SET @tabla_identidad = N'Empleados';
		INSERT INTO dbo.Empleados (ID_Empleado, Nombre_Completo, Estado)
		SELECT -1000 - ID_Trabajador, N'Asignación temporal', N'Activo' FROM dbo.Trabajadores
		UNION ALL SELECT -2001, N'Asignación temporal', N'Activo';
		SET IDENTITY_INSERT dbo.Empleados OFF;
		SET @tabla_identidad = NULL;

		UPDATE dbo.Trabajadores SET ID_Empleado = -1000 - ID_Trabajador;
		UPDATE dbo.Administrador SET ID_Empleado = -2001 WHERE ID_Administrador = 1;

		UPDATE e SET Nombre_Completo = p.nombre
		FROM dbo.Empleados e JOIN @personal p ON p.id_empleado = e.ID_Empleado;
		UPDATE dbo.Empleados SET Nombre_Completo = N'Administrador General' WHERE ID_Empleado = 1;

		SET IDENTITY_INSERT dbo.Empleados ON;
		SET @tabla_identidad = N'Empleados';
		INSERT INTO dbo.Empleados (ID_Empleado, Nombre_Completo, Estado)
		SELECT p.id_empleado, p.nombre, N'Activo' FROM @personal p
		WHERE NOT EXISTS (SELECT 1 FROM dbo.Empleados e WHERE e.ID_Empleado = p.id_empleado);
		SET IDENTITY_INSERT dbo.Empleados OFF;
		SET @tabla_identidad = NULL;

		UPDATE e SET Correo = c.Correo, Telefono = c.Telefono, Estado = c.Estado
		FROM dbo.Empleados e JOIN @personal p ON p.id_empleado = e.ID_Empleado
		JOIN #contactos c ON c.id_trabajador = p.id_trabajador;
		UPDATE e SET Correo = c.Correo, Telefono = c.Telefono, Estado = c.Estado
		FROM dbo.Empleados e CROSS JOIN #contacto_administrador c WHERE e.ID_Empleado = 1;
		DROP TABLE #contactos;
		DROP TABLE #contacto_administrador;

		UPDATE dbo.Roles_Sistema SET Nombre_Rol = N'Trabajador' WHERE ID_Rol = 1;
		UPDATE dbo.Roles_Sistema SET Nombre_Rol = N'Administrador' WHERE ID_Rol = 2;

		SET IDENTITY_INSERT dbo.Trabajadores ON;
		SET @tabla_identidad = N'Trabajadores';
		INSERT INTO dbo.Trabajadores (ID_Trabajador, ID_Empleado, Rol_Cargo, HoraIngreso, Codigo_Trabajador, PIN_Acceso, ID_Rol)
		SELECT p.id_trabajador, p.id_empleado, p.cargo, t.HoraIngreso, p.codigo, t.PIN_Acceso, 1
		FROM @personal p CROSS JOIN dbo.Trabajadores t
		WHERE p.id_trabajador = 5 AND t.ID_Trabajador = 4;
		SET IDENTITY_INSERT dbo.Trabajadores OFF;
		SET @tabla_identidad = NULL;

		UPDATE t SET ID_Empleado = p.id_empleado, Rol_Cargo = p.cargo, Codigo_Trabajador = p.codigo, ID_Rol = 1
		FROM dbo.Trabajadores t JOIN @personal p ON p.id_trabajador = t.ID_Trabajador;
		UPDATE dbo.Administrador SET ID_Empleado = 1, ID_Rol = 2, Codigo_Administrador = N'AD001'
		WHERE ID_Administrador = 1;

		UPDATE dbo.Asistencia SET ID_Trabajador = 5 WHERE ID_Trabajador = 4;
		UPDATE dbo.Tareas SET ID_Trabajador = 5 WHERE ID_Trabajador = 4;
		UPDATE dbo.Archivos SET ID_Trabajador = 5 WHERE ID_Trabajador = 4;
		UPDATE dbo.Evaluaciones_Rendimiento SET ID_Trabajador = 5 WHERE ID_Trabajador = 4;
		UPDATE dbo.Tareas SET Descripcion_Tarea = REPLACE(Descripcion_Tarea, N' / TR-004', N' / TR-005')
		WHERE ID_Trabajador = 5 AND Descripcion_Tarea =
			N'Revisión del expediente diario ' + CONVERT(nvarchar(8), Fecha, 112) + N' / TR-004';

		DELETE FROM dbo.Trabajadores WHERE ID_Trabajador = 4;
		DELETE FROM dbo.Empleados WHERE ID_Empleado = 5 OR ID_Empleado BETWEEN -1011 AND -1001 OR ID_Empleado = -2001;
		DELETE FROM dbo.Roles_Sistema WHERE ID_Rol = 3
			AND NOT EXISTS (SELECT 1 FROM dbo.Trabajadores WHERE ID_Rol = 3)
			AND NOT EXISTS (SELECT 1 FROM dbo.Administrador WHERE ID_Rol = 3);

		UPDATE [A&SG_DataMart].dbo.dim_trabajador SET id_trabajador_origen = 5
		WHERE id_trabajador_origen = 4;
	END;

	IF (SELECT COUNT(*) FROM dbo.Trabajadores) <> 10
		OR EXISTS (
			SELECT 1 FROM @personal p
			LEFT JOIN dbo.Trabajadores t ON t.ID_Trabajador = p.id_trabajador
			LEFT JOIN dbo.Empleados e ON e.ID_Empleado = t.ID_Empleado
			WHERE t.ID_Trabajador IS NULL OR t.ID_Empleado <> p.id_empleado
				OR e.Nombre_Completo <> p.nombre OR t.Codigo_Trabajador <> p.codigo OR t.ID_Rol <> 1
		)
		OR NOT EXISTS (SELECT 1 FROM dbo.Administrador WHERE ID_Administrador = 1 AND ID_Empleado = 1 AND ID_Rol = 2)
		THROW 50502, N'El padrón no coincide con el origen. Se revirtió la operación.', 1;

	IF @asistencias_antes <> (SELECT COUNT(*) FROM dbo.Asistencia)
		OR @tareas_antes <> (SELECT COUNT(*) FROM dbo.Tareas)
		THROW 50503, N'Las cantidades históricas cambiaron. Se revirtió la operación.', 1;

	COMMIT TRANSACTION;
END TRY
BEGIN CATCH
	IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
	IF @tabla_identidad IS NOT NULL
	BEGIN
		DECLARE @sentencia nvarchar(300) = N'SET IDENTITY_INSERT dbo.' + QUOTENAME(@tabla_identidad) + N' OFF;';
		EXEC sys.sp_executesql @sentencia;
	END;
	THROW;
END CATCH;

SELECT t.ID_Trabajador, e.ID_Empleado, e.Nombre_Completo, t.Rol_Cargo, t.Codigo_Trabajador
FROM dbo.Trabajadores t JOIN dbo.Empleados e ON e.ID_Empleado = t.ID_Empleado
ORDER BY t.ID_Trabajador;
GO

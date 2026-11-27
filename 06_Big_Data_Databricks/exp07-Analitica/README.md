# Guía de ejecución · EXP-07 Consulta analítica con join: IEP por trabajador

Proyecto: Base de Datos Avanzadas y Big Data · Grupo 2 · UPN
Carpeta del repositorio: `06_Big_Data_Databricks/exp07-Analitica`
Datos: `asistencias_15000.csv` y `tareas_15000.csv` (15 000 filas cada uno, datos sintéticos)

Esta guía te lleva de la mano **desde que entras a Databricks hasta el último resultado**. No necesitas saber programar: solo leer con calma, copiar, pegar y mirar qué sale.

---

## 0. ¿Qué vamos a hacer?

Imagina que eres el profesor y tienes **dos listas**: una de **asistencias** (quién llegó a tiempo) y otra de **tareas** (quién entregó bien y a tiempo). Para poner la "libreta de notas" de cada trabajador tienes que **juntar las dos listas por su nombre**. Eso se llama **join** (unir): juntamos las dos tablas usando la columna que tienen en común, `ID_Trabajador`.

Con eso calculamos 4 indicadores (*KPI*) por trabajador:

| KPI | Qué mide | Cómo se calcula |
|---|---|---|
| **TPA** · Tasa de puntualidad | Qué porcentaje de días llegó a tiempo (hasta las 09:40:59) | asistencias "A tiempo" ÷ total de asistencias × 100 |
| **ICT** · Índice de cumplimiento de tareas | Qué porcentaje de tareas terminó sin observaciones | tareas "Completada" sin observación ÷ total de tareas × 100 |
| **TDT** · Tasa de devolución de tareas | Qué porcentaje entregó fuera de plazo | tareas con `[ENTREGADO FUERA DE PLAZO]` ÷ total de tareas × 100 |
| **IEP** · Índice de efectividad ponderado | La "nota final" de 0 a 100 | `TPA × 0,30 + ICT × 0,50 + (100 − TDT) × 0,20` |

> 💡 En el IEP la TDT se resta de 100 porque **entregar fuera de plazo es malo**: mientras menos entregas tardías, más puntos.

La misma cuenta se puede escribir de dos formas: con **DataFrame API** (funciones de Python) o con **Spark SQL** (preguntas en SQL). También probamos **`cache()`**, que es como dejar los datos **en la mesa** en vez de ir a buscarlos al estante cada vez.

**La pregunta del experimento:** ¿Calcular los KPI de los 262 trabajadores es **más rápido** con DataFrame API, con Spark SQL o usando caché? ¿Las dos formas dan **el mismo resultado**?

**El camino completo (mapa):**

```
 1. Entrar a Databricks
 2. Crear el ESQUEMA      (el estante)
 3. Crear el VOLUMEN      (la caja dentro del estante)
 4. Crear el DIRECTORIO   (la carpeta dentro de la caja)
 5. Subir los 2 CSV       (las hojas dentro de la carpeta)
 6. Crear el NOTEBOOK     (el cuaderno donde escribimos órdenes)
 7. Aprender a usar celdas
 8. Ejecutar las celdas del experimento, una por una
 9. Hacer los gráficos
10. Escribir la conclusión y tomar las capturas
```

> 💡 **Idea clave:** Databricks es como una **cocina enorme en internet**. Tú escribes la receta (los comandos) y Databricks la cocina con **Apache Spark**, un motor que sabe repartir el trabajo entre muchas computadoras a la vez. Así se procesa mucha información rápido. Eso es *Big Data*.

---

## 1. Antes de empezar: ¿qué necesitas?

| Necesitas | Para qué |
|---|---|
| Una computadora con internet y un navegador (Chrome o Edge) | Databricks funciona dentro del navegador; no se instala nada |
| Un correo (Gmail sirve) | Para tu cuenta gratuita de Databricks |
| Los archivos `asistencias_15000.csv` y `tareas_15000.csv` | Son los datos del experimento. Vienen en `Experimentos_15000.zip`, que comparte el grupo. Descomprímelo en tu computadora |
| 40 a 60 minutos sin apuro | Algunas celdas tardan un poco en terminar |

> ⚠️ **Sube solo los dos CSV.** El zip también trae `manifiesto_15000.csv`, `generar_15000.py` y una guía. Esos **no** se suben: el manifiesto es solo la "etiqueta" que dice cuántas filas tiene cada archivo y su huella digital (SHA-256), para comprobar que nadie los cambió.

**Todos los integrantes usan los mismos dos CSV.** Lo que cambia es el experimento que hace cada uno.

---

## 2. Paso 1 · Entrar a Databricks (login)

1. Abre el navegador y entra a <https://www.databricks.com/learn/free-edition>.
2. **Si es tu primera vez:** pulsa **Sign up** (registrarse).
   **Si ya tienes cuenta:** pulsa **Log in** (iniciar sesión).
3. Elige **Continue with Google** (continuar con Google) o escribe tu correo.
4. Si escribiste tu correo, Databricks te manda un **código** a tu bandeja. Ábrelo y cópialo en la página. (Ese código es solo tuyo: no se lo pases a nadie.)
5. Llegarás a la página de inicio, llamada **Home**. A la izquierda verás un menú con opciones como **Workspace**, **Catalog** y **New**.

> 💡 Databricks está en inglés. En esta guía cada botón lleva su traducción entre paréntesis.
> La edición gratuita (*Free Edition*) no pide tarjeta y ya trae el computador listo, llamado **Serverless** (sin servidor que tengas que encender tú).

📸 **No hace falta captura** de este paso. Nunca captures la pantalla donde aparece tu correo o tu código.

---

## 3. Paso 2 · Crear el esquema (el estante)

Un **esquema** es como un **estante de una biblioteca**: ahí ponemos todo lo de un mismo tema (tablas y archivos). Cada experimento tiene su propio estante, para no mezclar cosas.

1. En el menú izquierdo pulsa **Catalog** (catálogo). Es el "explorador" de datos.
2. En la lista, haz clic en el catálogo **workspace**.
3. Arriba a la derecha pulsa **Create schema** (crear esquema).
4. En **Schema name** (nombre del esquema) escribe: **`exp07_analitica`**
5. Pulsa **Create** (crear).

> ⚠️ **Reglas para el nombre:** solo letras minúsculas, números y guion bajo `_`.
> **Sin tildes, sin espacios y sin guion medio `-`.** Por ejemplo `analítica` o `particion-ana` darán problemas después (el código necesitaría unas comillas especiales `` ` `` para entenderlos).
> Si el nombre ya existe, agrégale tu nombre: `exp07_analitica_tunombre`. **Si cambias el nombre, anótalo**: lo usarás en el Paso 8.

---

## 4. Paso 3 · Crear el volumen (la caja)

Un **volumen** es como una **caja dentro del estante** donde se guardan **archivos** (por ejemplo, los CSV). Las tablas van sueltas en el estante; los archivos van en la caja.

1. Dentro del Catalog, haz clic en tu esquema **`exp07_analitica`**.
2. Arriba a la derecha pulsa **Create** (crear) → **Volume** (volumen).
3. En **Volume name** escribe: **`vol_analitica`**
4. Deja el tipo en **Managed volume** (volumen administrado: Databricks lo cuida por ti).
5. Pulsa **Create**.

---

## 5. Paso 4 · Crear el directorio (la carpeta)

Un **directorio** es una **carpeta dentro de la caja**, para tener todo ordenado.

1. Haz clic en tu volumen **`vol_analitica`**.
2. Pulsa **Create directory** (crear directorio). Si no lo ves, búscalo en el menú **⋮** (tres puntos).
3. Escribe: **`datos`** y pulsa **Create**.

---

## 6. Paso 5 · Subir los dos CSV

1. Entra a la carpeta **`datos`** (haz clic en ella).
2. Pulsa **Upload to this volume** (subir a este volumen).
3. Arrastra `asistencias_15000.csv` y `tareas_15000.csv` al recuadro (o pulsa **Browse** para buscarlos).
4. Pulsa **Upload** (subir) y espera a que terminen.
5. Comprueba que aparecen los dos, con tamaño aproximado de **1 MB** cada uno.

**¿Dónde quedaron?** Cada archivo ahora tiene una **ruta**, que es como su dirección postal:

```
/Volumes/workspace/exp07_analitica/vol_analitica/datos/asistencias_15000.csv
```

| Parte de la ruta | Qué es |
|---|---|
| `/Volumes` | La zona de Databricks donde viven los archivos |
| `workspace` | El catálogo (la biblioteca completa) |
| `exp07_analitica` | Tu esquema (el estante) |
| `vol_analitica` | Tu volumen (la caja) |
| `datos` | Tu directorio (la carpeta) |
| `asistencias_15000.csv` | El archivo (la hoja) |

> 💡 Si haces clic en un archivo, Databricks muestra un botón para **copiar la ruta**. Es la forma más segura de no equivocarse con una letra.
> Las rutas distinguen **mayúsculas y minúsculas**: `datos` y `Datos` son carpetas distintas.

📸 **Captura 1:** el Catalog mostrando el esquema, el volumen, la carpeta `datos` y los dos CSV.

---

## 7. Paso 6 · Crear el notebook (el cuaderno)

Un **notebook** es un **cuaderno digital**. Está hecho de **celdas**: recuadros donde escribes una orden, la ejecutas y debajo aparece el resultado. Es como un cuaderno de laboratorio donde cada experimento queda anotado con su resultado.

1. En el menú izquierdo pulsa **+ New** (nuevo) → **Notebook**.
2. Arriba, haz clic en el título (dice algo como *Untitled Notebook…*) y cámbialo a: **`EXP07_Analitica`**
3. Al lado del título debe decir **Python**. Si no, cámbialo a Python.
4. Arriba a la derecha está el botón del computador. Debe decir **Serverless** con un **punto verde**. Si dice **Connect** (conectar), púlsalo y elige **Serverless**.

---

## 8. Paso 7 · Mini clase: cómo se usan las celdas

### Agregar una celda
Pasa el mouse **debajo de la última celda**: aparecen dos botones.
- **+ Code** → celda de **código** (órdenes para la computadora).
- **+ Text** → celda de **texto** (explicaciones para personas).

### Ejecutar una celda
- Haz clic dentro de la celda y pulsa **Shift + Enter** (mantén Shift y aprieta Enter).
- O pulsa el botón **▶** que aparece a la izquierda de la celda.
- Mientras trabaja verás un círculo girando. Cuando termina aparece un **✓ verde** con la hora.

### La primera línea manda
La **primera línea** de la celda le dice a Databricks en qué "idioma" está escrita:

| Primera línea | Idioma | Para qué |
|---|---|---|
| (nada especial, o una línea que empieza con `#`) | **Python** | La mayoría de las celdas |
| `%sql` | **SQL** | Preguntas a una tabla, como "¿cuántos hay de cada tipo?" |
| `%md` | **Markdown** (texto) | Títulos y explicaciones |

> 💡 En Python, una línea que empieza con `#` es un **comentario**: la computadora lo ignora. Sirve para que las personas entiendan qué hace la celda. Cada celda de esta guía empieza con un comentario que funciona como su **título**.

### Las 4 reglas de oro
1. **Una celda por bloque.** Cada recuadro de código de esta guía va en **su propia celda**.
2. **En orden, de arriba hacia abajo.** Cada celda usa cosas que creó la anterior. Es como una receta: no puedes hornear antes de mezclar.
3. **Espera el ✓ verde** antes de ejecutar la siguiente.
4. **Si cierras la página o se reinicia el computador,** Databricks "olvida" lo que había en memoria: vuelve a ejecutar **desde la celda 2**.

📸 **Captura 2:** la parte de arriba del notebook con el nombre y el botón **Serverless** conectado.

---

## 9. Paso 8 · Las celdas del experimento

Copia cada bloque en una celda nueva y ejecútalo. Debajo de cada uno te explico **qué hace** y **qué debe salir**.

### Celda 1 · Portada (celda de texto)

```
%md
# EXP-07 · Consulta analítica con join: IEP por trabajador
**Objetivo:** comparar el tiempo de calcular TPA, ICT, TDT e IEP por trabajador (join de asistencias y tareas) con DataFrame API y con Spark SQL, y evaluar el efecto de cache().
**Configuración:** Databricks Free Edition, compute serverless, esquema exp07_analitica, 1 calentamiento + 5 repeticiones por variante, una ejecución a la vez.
**Arquitectura:** CSV → Volume (datos) → DataFrames → tablas Delta → agregación + join por trabajador (API y SQL) → ranking de IEP → gráficos.
```

**¿Qué hace?** Es la **portada** del cuaderno: dice qué vamos a investigar. Como empieza con `%md`, Databricks la muestra como texto con formato, no como código.

**¿Qué debe salir?** Un título grande y tres líneas de texto.

📸 **Captura:** la portada (sirve como evidencia del **objetivo** y la **configuración**).
### Celda 2 · Configuración (las direcciones)

```python
# Celda 2 · Configuración: dónde está mi estante y dónde están mis archivos
sch  = "workspace.exp07_analitica"
base = "/Volumes/workspace/exp07_analitica/vol_analitica/datos"
```

**¿Qué hace?** Guarda en **variables** las direcciones que usaremos todo el tiempo. Una variable es como una **cajita con nombre**: en `sch` guardamos el nombre del estante y en `base` la dirección de la carpeta de los CSV. Así no escribimos la dirección larga en cada celda.

**¿Qué debe salir?** Nada, solo el ✓ verde. Es normal.

> ⚠️ Si en los Pasos 2, 3 o 4 usaste otros nombres, **cámbialos aquí**, dentro de las comillas.
### Celda 3 · Mirar los archivos por dentro

```python
# Celda 3 · Mostrar las primeras líneas de los dos CSV
print(dbutils.fs.head(f"{base}/asistencias_15000.csv", 500))
print(dbutils.fs.head(f"{base}/tareas_15000.csv", 500))
```

**¿Qué hace?** Abre cada archivo y muestra solo el **comienzo** (los primeros 500 caracteres), como cuando hojeas la primera página de un libro. `print` significa "muéstralo en pantalla".

**¿Qué debe salir?** La primera fila con los **nombres de las columnas** (`ID_Asistencia,ID_Trabajador,Fecha_Entrada,...` y `ID_Tarea,ID_Trabajador,ID_Proyecto,...`) y debajo algunas filas de datos.

> 💡 En clase se usaba `%fs head`. El computador Serverless no lo acepta, por eso usamos `dbutils.fs.head`, que hace lo mismo.

📸 **Captura:** esta celda con su resultado.
### Celda 4 · Cargar los datos en DataFrames

```python
# Celda 4 · Cargar los dos CSV en DataFrames con su esquema (lista de columnas y tipos)
from pyspark.sql.types import *
esq_a = StructType([StructField("ID_Asistencia", IntegerType()), StructField("ID_Trabajador", IntegerType()),
    StructField("Fecha_Entrada", TimestampType()), StructField("Fecha_Salida", TimestampType()),
    StructField("Fecha_Calculada", DateType()), StructField("Estado_Asistencia", StringType())])
esq_t = StructType([StructField("ID_Tarea", IntegerType()), StructField("ID_Trabajador", IntegerType()),
    StructField("ID_Proyecto", IntegerType()), StructField("Fecha", DateType()),
    StructField("Fecha_Inicio", TimestampType()), StructField("Fecha_Entrega", TimestampType()),
    StructField("Estado_Tarea", StringType()), StructField("Observaciones", StringType())])
dfAsistencias = spark.read.csv(f"{base}/asistencias_15000.csv", header=True, schema=esq_a)
dfTareas      = spark.read.csv(f"{base}/tareas_15000.csv", header=True, schema=esq_t)
print("Filas cargadas:", dfAsistencias.count(), dfTareas.count())
display(dfAsistencias)
```

**¿Qué hace?**
- Primero escribe el **esquema de datos**: una lista que dice qué tipo de dato tiene cada columna. Es como poner etiquetas en los cajones: este es de **números** (`IntegerType`), este de **fecha y hora** (`TimestampType`), este de **fecha** (`DateType`), este de **texto** (`StringType`).
- Luego lee los CSV y los convierte en **DataFrames**: tablas que Spark tiene en memoria, listas para trabajar.
- `header=True` le avisa que la primera fila son los **títulos**, no datos.
- `count()` cuenta las filas y `display()` muestra la tabla bonita.

**¿Qué debe salir?** `Filas cargadas: 15000 15000` y una tabla de 6 columnas.

📸 **Captura:** esta celda con el conteo y la tabla.

### Celda 5 · Revisar y limpiar los datos (EDA)

```python
# Celda 5 · EDA y limpieza: resumen, vacíos, observaciones, horas coherentes y nombre de columna
from pyspark.sql.functions import col, sum as fsum, when
display(dfAsistencias.describe())
display(dfTareas.select([fsum(when(col(c).isNull(), 1).otherwise(0)).alias(c) for c in dfTareas.columns]))
display(dfTareas.filter(col("Observaciones").isNotNull()).groupBy("Observaciones").count())
print("Salida antes de entrada:", dfAsistencias.filter(col("Fecha_Salida") < col("Fecha_Entrada")).count())
dfTareas = dfTareas.withColumnRenamed("Observaciones", "Observacion")
```

**¿Qué hace?** **EDA** es el *análisis exploratorio de datos*: antes de cocinar, revisamos los ingredientes.
1. Resumen de asistencias.
2. Cuenta las **casillas vacías** (*nulos*) de cada columna de tareas.
3. Muestra qué **observaciones** distintas existen y cuántas veces aparece cada una.
4. Revisa que nadie haya **salido antes de entrar**.
5. Cambia el nombre `Observaciones` por `Observacion` (eso es **limpieza**).

**¿Qué debe salir?**
- Vacíos en tareas: `Fecha_Inicio` **2 057**, `Fecha_Entrega` **4 848**, `Observaciones` **13 106**; las demás, 0.
- Observaciones: **2 textos**. Uno pide corregir medidas (**1 349** tareas) y el otro es `[ENTREGADO FUERA DE PLAZO]` (**545** tareas). Este último es el que usa la TDT.
- `Salida antes de entrada: 0`

> 💡 Que haya vacíos **es normal**: una tarea "Asignada" todavía no empezó, así que no tiene fecha de inicio.

📸 **Captura:** esta celda con sus resultados.

### Celda 6 · Contar tareas por estado (para un gráfico)

```python
# Celda 6 · Tareas por estado, lista para graficar
display(dfTareas.groupBy("Estado_Tarea").count().withColumnRenamed("count", "cantidad"))
```

**¿Qué debe salir?** Completada **10 452**, En Progreso **2 521**, Asignada **2 027**. Sobre ella harás el **Gráfico 1**.

### Celda 7 · Guardar como tablas permanentes

```python
# Celda 7 · Guardar las dos tablas Delta en el esquema
dfAsistencias.write.mode("overwrite").saveAsTable(f"{sch}.tb_asistencias")
dfTareas.write.mode("overwrite").saveAsTable(f"{sch}.tb_tareas")
```

**¿Qué hace?** Pasa los datos de la **memoria** (la pizarra) a **tablas Delta** permanentes (el cuaderno). `overwrite` = "si ya existe, reemplázala".
**¿Qué debe salir?** Solo el ✓. En el Catalog aparecen `tb_asistencias` y `tb_tareas`.

📸 **Captura:** el Catalog con las dos tablas.

### Celda 8 · Pregunta con SQL: ¿cuántas tareas hay de cada estado?

```sql
%sql
-- Celda 8 · Contar tareas por estado con COUNT + GROUP BY, de mayor a menor
SELECT Estado_Tarea, COUNT(*) AS cantidad
FROM workspace.exp07_analitica.tb_tareas
GROUP BY Estado_Tarea
ORDER BY cantidad DESC
```

**¿Qué hace?** **SQL** es un idioma para preguntarle cosas a las tablas: `SELECT` (muéstrame), `FROM` (de esta tabla), `GROUP BY` (agrupando los iguales, como separar fichas por color) y `ORDER BY ... DESC` (del mayor al menor).
**¿Qué debe salir?** Completada **10452**, En Progreso **2521**, Asignada **2027**.

> ⚠️ Esta celda **sí** empieza con `%sql`. Si tu esquema tiene otro nombre, cámbialo en `FROM`. Si lleva tilde (por ejemplo `analítica`), escríbelo entre comillas invertidas: `` workspace.`exp07_analítica`.tb_tareas ``.

📸 **Captura:** esta celda.

### Celda 9 · Escribir la "libreta de notas" de dos formas

```python
# Celda 9 · Calcular TPA, ICT, TDT e IEP por trabajador con DataFrame API (A) y con Spark SQL (B)
from pyspark.sql.functions import count
def iep_df():
    a = dfAsistencias.groupBy("ID_Trabajador").agg(
        count("*").alias("asist"), fsum(when(col("Estado_Asistencia") == "A tiempo", 1).otherwise(0)).alias("punt"))
    t = dfTareas.groupBy("ID_Trabajador").agg(
        count("*").alias("tareas"),
        fsum(when((col("Estado_Tarea") == "Completada") & col("Observacion").isNull(), 1).otherwise(0)).alias("sin_obs"),
        fsum(when(col("Observacion").contains("FUERA DE PLAZO"), 1).otherwise(0)).alias("fuera"))
    return (a.join(t, "ID_Trabajador")
             .withColumn("TPA", 100 * col("punt") / col("asist"))
             .withColumn("ICT", 100 * col("sin_obs") / col("tareas"))
             .withColumn("TDT", 100 * col("fuera") / col("tareas"))
             .withColumn("IEP", col("TPA") * 0.30 + col("ICT") * 0.50 + (100 - col("TDT")) * 0.20))
dfAsistencias.createOrReplaceTempView("v_asist"); dfTareas.createOrReplaceTempView("v_tareas")
q_sql = """
WITH a AS (SELECT ID_Trabajador, COUNT(*) asist, SUM(CASE WHEN Estado_Asistencia = 'A tiempo' THEN 1 ELSE 0 END) punt
           FROM v_asist GROUP BY ID_Trabajador),
t AS (SELECT ID_Trabajador, COUNT(*) tareas,
             SUM(CASE WHEN Estado_Tarea = 'Completada' AND Observacion IS NULL THEN 1 ELSE 0 END) sin_obs,
             SUM(CASE WHEN Observacion LIKE '%FUERA DE PLAZO%' THEN 1 ELSE 0 END) fuera
      FROM v_tareas GROUP BY ID_Trabajador)
SELECT a.ID_Trabajador, 100.0*punt/asist TPA, 100.0*sin_obs/tareas ICT, 100.0*fuera/tareas TDT,
       0.3*(100.0*punt/asist) + 0.5*(100.0*sin_obs/tareas) + 0.2*(100 - 100.0*fuera/tareas) IEP
FROM a JOIN t USING (ID_Trabajador)"""
print("Trabajadores (API):", iep_df().count(), "| (SQL):", spark.sql(q_sql).count())
```

**¿Qué hace?** Escribe **la misma receta dos veces**, en dos "idiomas":
- **Forma A · DataFrame API** (`iep_df`): con funciones de Python. Primero cuenta por trabajador sus asistencias y puntualidades (`a`), luego sus tareas, las completadas sin observación y las fuera de plazo (`t`). Después las **une** con `join` por `ID_Trabajador` y calcula los 4 KPI.
- **Forma B · Spark SQL** (`q_sql`): la misma cuenta escrita como pregunta SQL. `createOrReplaceTempView` le pone un **nombre temporal** a cada DataFrame para que SQL pueda usarlo.

**¿Qué debe salir?** `Trabajadores (API): 262 | (SQL): 262`. Las dos formas encontraron a los mismos 262 trabajadores.

📸 **Captura:** esta celda.

### Celda 10 · Validación: ¿las dos formas dan la misma nota?

```python
# Celda 10 · Validación: top 5 de IEP y KPI globales; deben coincidir en las dos formas
display(iep_df().orderBy(col("IEP").desc(), "ID_Trabajador").limit(5))
display(spark.sql(q_sql + " ORDER BY IEP DESC, ID_Trabajador LIMIT 5"))
g = iep_df().agg(fsum("punt").alias("p"), fsum("asist").alias("a"), fsum("sin_obs").alias("s"),
                 fsum("fuera").alias("f"), fsum("tareas").alias("t")).collect()[0]
TPA, ICT, TDT = 100 * g.p / g.a, 100 * g.s / g.t, 100 * g.f / g.t
print(round(TPA, 2), round(ICT, 2), round(TDT, 2), round(0.3 * TPA + 0.5 * ICT + 0.2 * (100 - TDT), 2))
```

**¿Qué hace?** Antes de cronometrar, revisamos que las dos formas digan **lo mismo**: muestra los **5 mejores** según cada forma y calcula los KPI de **toda la empresa**.

**¿Qué debe salir?**
- Las dos tablas iguales: los trabajadores **2, 1163, 1173, 1177 y 1180**, todos con IEP **96,00**. (En total hay 16 empatados en 96; el orden por `ID_Trabajador` decide cuáles 5 se muestran.)
- La línea `92.46 57.05 3.63 75.54` (TPA, ICT, TDT e IEP global).

Si algo no coincide, **no reportes los tiempos** y avisa al grupo.

📸 **Captura:** esta celda.

### Celda 11 · ¡El experimento! Cronometrar las dos formas y la caché

```python
# Celda 11 · Medir A (DataFrame API), B (Spark SQL) y C (API con cache): 1 calentamiento + 5 repeticiones
import time, statistics as st, pandas as pd
def medir(fn, n=5):
    fn(); t = []                                    # 1.ª vez = calentamiento (no se cuenta)
    for _ in range(n):
        s = time.perf_counter(); fn(); t.append(time.perf_counter() - s)
    return t
res = []
for nombre, fn in [("A_DataFrame", lambda: iep_df().collect()), ("B_SparkSQL", lambda: spark.sql(q_sql).collect())]:
    t = medir(fn); res.append((nombre, st.median(t), min(t), max(t)))
try:
    dfAsistencias.cache().count(); dfTareas.cache().count()      # C: datos guardados "en la mesa"
    t = medir(lambda: iep_df().collect()); res.append(("C_DataFrame_cache", st.median(t), min(t), max(t)))
except Exception as e:
    print("cache() no disponible en este compute:", str(e)[:200])    # también es un resultado: se reporta tal cual
dfRes = spark.createDataFrame(pd.DataFrame(res, columns=["variante", "mediana_s", "minimo_s", "maximo_s"]))
display(dfRes)
```

**¿Qué hace?** Cronometra la forma **A**, la forma **B** y luego la **C**: la forma A pero con los datos en **caché** (en la mesa, listos para usar).

> 💡 **¿Cómo medimos el tiempo?** La función `medir` hace lo que haría un entrenador con un cronómetro:
> 1. Primero hace una **vuelta de calentamiento** que no se cuenta, porque la primera siempre sale más lenta.
> 2. Después repite **5 veces** y anota cuánto tardó cada vez (`time.perf_counter()` es el cronómetro).
> 3. Al final reportamos la **mediana** (el tiempo del medio), el **mínimo** y el **máximo**. Usamos la mediana porque no la arruina una vuelta rara.
>
> **Mientras corre esta celda no ejecutes nada más**, porque eso alteraría el cronómetro.
>
> `try` / `except` significa "**intenta** esto y, **si falla**, no te detengas: avisa y sigue". Lo usamos porque en Serverless `cache()` solo funciona en algunas versiones del entorno.

**¿Qué debe salir?** Una tabla con **3 filas** (A, B y C) o con **2 filas** (A y B) más un mensaje `cache() no disponible...`. Las dos situaciones son válidas: si sale el mensaje, **cópialo** y menciónalo como limitación. Los segundos **no tienen un valor fijo**.

📸 **Captura:** esta celda con la tabla (es el **resultado** principal).

### Celda 12 · Agrupar trabajadores por rango de IEP (para un gráfico)

```python
# Celda 12 · Cantidad de trabajadores por rango de IEP
r = iep_df().withColumn("rango_IEP",
        when(col("IEP") < 25, "1) 0-25").when(col("IEP") < 50, "2) 25-50")
        .when(col("IEP") < 75, "3) 50-75").when(col("IEP") < 90, "4) 75-90").otherwise("5) 90-100"))
display(r.groupBy("rango_IEP").count().withColumnRenamed("count", "trabajadores").orderBy("rango_IEP"))
```

**¿Qué hace?** Pone a cada trabajador en un "grupo de notas", como separar exámenes en montones: de 0 a 25, de 25 a 50, de 50 a 75, de 75 a 90 y de 90 a 100. `when` significa "cuando pase esto, ponle esta etiqueta".

**¿Qué debe salir?** 5 filas con **10, 18, 37, 169 y 28** trabajadores (suman **262**). Sobre ella harás el **Gráfico 3**.

### Valores de control de EXP-07 (si no salen, hay un error)

| Celda | Valor esperado |
|---|---|
| 4 | `Filas cargadas: 15000 15000` |
| 5 | Vacíos: `Fecha_Inicio` 2 057 · `Fecha_Entrega` 4 848 · `Observaciones` 13 106 · observaciones 1 349 y 545 |
| 6 y 8 | Completada 10 452 · En Progreso 2 521 · Asignada 2 027 |
| 9 | `Trabajadores (API): 262 \| (SQL): 262` |
| 10 | Top 5: 2 · 1163 · 1173 · 1177 · 1180 (IEP 96,00) · `92.46 57.05 3.63 75.54` |
| 12 | 10 · 18 · 37 · 169 · 28 (total 262) |
| 11 | Los segundos **no** tienen un valor fijo: anota los tuyos |
---

## 10. Paso 9 · Los gráficos (visualizaciones)

Un gráfico convierte una tabla de números en un **dibujo** que se entiende de un vistazo. El profesor pide que cada gráfico vaya acompañado de una **breve explicación** de lo que demuestra.

### ¿Cómo se crea un gráfico en Databricks?

1. Debajo del resultado de la celda aparece una tabla. Arriba de esa tabla hay una pestaña que dice **Table** (tabla) y, a su lado, un botón **+**.
2. Pulsa **+** → **Visualization** (visualización).
3. En **Visualization type** (tipo de gráfico) elige **Bar** (barras).
4. En **X column** elige la columna que va **abajo** (las categorías).
5. En **Y columns** elige los números que dan la **altura** de las barras. Si aparece **Sum**, déjalo así.
6. En la pestaña **X axis** y **Y axis** puedes poner el **nombre de los ejes** (*Name*).
7. En la pestaña **Data labels** activa **Show data labels** (mostrar números sobre las barras).
8. Pulsa **Save** (guardar). Puedes cambiar el nombre de la pestaña del gráfico haciendo doble clic sobre ella.
9. Debajo del gráfico agrega una celda **+ Text** y escribe qué demuestra (te dejo el texto listo para completar).

### Gráfico 1 · Tareas por estado (sobre la Celda 6)
- X column: `Estado_Tarea` · Y columns: `cantidad` · Data labels: activados

```
%md
**Qué demuestra:** cuántas de las 15 000 tareas están completadas, en progreso o asignadas.
Lectura: predominan las tareas completadas (10 452), que son la base del ICT.
```

### Gráfico 2 · Tiempo de cálculo por forma (sobre la Celda 11)
- X column: `variante` · Y columns: `mediana_s`, `minimo_s` y `maximo_s` (sin apilar: *Stacking* desactivado)
- Ejes: `Variante de cálculo` y `Tiempo de cálculo (s)` · Data labels `0.000`
- En la pestaña **Series** renombra las barras como `Mediana`, `Mínimo` y `Máximo`
- Nombre de la pestaña: `Tiempo de cálculo del IEP por variante`

```
%md
**Qué demuestra:** cuánto tarda calcular TPA, ICT, TDT e IEP de los 262 trabajadores con DataFrame API, con Spark SQL y con caché.
Mediana: DataFrame ... s · SQL ... s · DataFrame con caché ... s.
Lectura: DataFrame API y Spark SQL pasan por el mismo optimizador de Spark (Catalyst), por eso se esperan tiempos parecidos. Las dos dieron el mismo ranking y los mismos KPI globales.
```

### Gráfico 3 · Trabajadores por rango de IEP (sobre la Celda 12)
- X column: `rango_IEP` · Y columns: `trabajadores`
- Ejes: `Rango de IEP (puntos)` y `Cantidad de trabajadores` · Data labels: activados
- Nombre de la pestaña: `Trabajadores por rango de IEP`

```
%md
**Qué demuestra:** cuántos trabajadores caen en cada nivel de IEP (nota de 0 a 100) con los datos sintéticos.
La mayoría (169 de 262) está entre 75 y 90 puntos; 28 superan los 90 y 10 están por debajo de 25.
Lectura: es un resultado de datos simulados con reglas definidas; no mide el desempeño laboral real.
```


---

## 11. Paso 10 · Conclusión, capturas y entrega

### Celda final · Comparación y análisis (celda de texto)

Agrega una celda **+ Text** al final y completa los `...` con **tus** números. No inventes valores: copia los que salieron en tu notebook.

```
%md
## Comparación y análisis
- Forma más rápida (mediana): ...  (segundos)
- ¿Ranking y KPI globales coinciden entre las dos formas?: sí / no
- ¿cache() estuvo disponible?: sí / no (si no, copiar el mensaje)
- Interpretación: DataFrame API y Spark SQL pasan por el mismo optimizador de Spark, por eso suelen dar tiempos casi iguales; cache() evita releer los datos cuando está disponible.
- Limitaciones: 15 000 filas, datos sintéticos, una sola sesión, compute serverless (no muestra uso de CPU ni RAM).
```

### Lista de capturas

El profesor pide documentar **objetivo, procedimiento y pasos, configuración, resultados, comparación y análisis** y **evidencias de ejecución**. En cada captura debe verse el **✓ verde con la hora**, y en ninguna debe aparecer tu correo.

- [ ] Catalog con esquema, volumen, carpeta `datos` y los 2 CSV (Paso 5)
- [ ] Notebook con su nombre y **Serverless** conectado (Paso 6)
- [ ] Celda 1 · portada
- [ ] Celda 3 · contenido de los archivos
- [ ] Celda 4 · DataFrames y conteo
- [ ] Celda 5 · EDA
- [ ] Celda 7 · tablas en el Catalog
- [ ] Celda 8 · consulta `GROUP BY`
- [ ] Celda 9 · 262 trabajadores en las dos formas
- [ ] Celda 10 · validación (top 5 y KPI globales)
- [ ] Celda 11 · tabla de tiempos
- [ ] Gráficos 1, 2 y 3 con su texto de "Qué demuestra"
- [ ] Celda final · comparación y análisis

Guarda las capturas en la carpeta `capturas/` de esta misma carpeta del repositorio. El nombre final de cada captura lo define el grupo al integrar el informe.

### Exportar y entregar
1. **Exportar el notebook:** arriba, **File** (archivo) → **Export** (exportar) → **HTML**. Ese archivo es la evidencia completa de que todo se ejecutó.
2. **Descargar la tabla de resultados:** la de la **Celda 11**. Debajo de la tabla, pulsa el botón de descarga (flecha ⤓) y elige **CSV**. Guárdala en la carpeta `archivos-csv/`.
3. Envía al responsable del informe: las capturas, el HTML y el CSV de resultados.

> ✅ **Antes de entregar, revisa:** que todas las celdas tengan ✓ verde, que los **valores de control** de esta guía coincidan con los tuyos y que la conclusión tenga tus números reales.
---

## Si algo sale mal

No te asustes: los errores son normales cuando se programa. Lee el mensaje **rojo** y busca aquí:

| Lo que dice el error | Qué significa | Cómo arreglarlo |
|---|---|---|
| `CloudFileNotFoundException`, *file not found* o *PATH_NOT_FOUND* | La computadora no encuentra el archivo: la ruta tiene algo mal escrito | Revisa la celda 2. Copia la ruta real desde el Catalog (Paso 5) y quítale el nombre del archivo del final |
| La ruta tiene una carpeta repetida, como `.../datos/datos/...` | Escribiste la carpeta dos veces | Deja la carpeta solo una vez en la ruta |
| `SyntaxError` (error de sintaxis) | Algo está mal escrito, como una palabra rota o la primera línea equivocada | Revisa que una celda de Python **no** empiece con `%sql`, y que no haya un `#` pegado a una palabra |
| `NameError: name '...' is not defined` | Usas algo que todavía no existe en memoria | Ejecuta otra vez desde la celda 2, en orden |
| `SCHEMA_NOT_FOUND` o `TABLE_OR_VIEW_NOT_FOUND` | El nombre del esquema o de la tabla no coincide | Revisa que el esquema de la celda 2 y del `%sql` sea exactamente el que creaste |
| La celda se queda en *Waiting* (esperando) varios minutos | El computador está ocupado o se desconectó | Pulsa **Interrupt** (interrumpir) y vuelve a ejecutarla |
| *Attached cluster is terminated* | El computador se apagó | Pulsa el botón del computador → **Serverless** → vuelve a ejecutar desde la celda 2 |

Si no se arregla, manda al grupo **una captura del mensaje de error completo y de la celda donde ocurrió**. No sigas con las celdas siguientes hasta resolverlo.

---

## Mini glosario

| Palabra | En simple |
|---|---|
| **Big Data** | Trabajar con muchos datos usando varias computadoras a la vez |
| **Apache Spark** | El motor que hace los cálculos repartiéndolos en partes |
| **Serverless** | El computador de Databricks que se conecta solo; no tienes que encenderlo |
| **Esquema** | El estante donde guardamos tablas y volúmenes de un tema |
| **Volumen** | La caja dentro del estante donde van los archivos |
| **Directorio** | Una carpeta dentro del volumen |
| **Ruta** | La dirección de un archivo, como `/Volumes/workspace/...` |
| **CSV** | Archivo de texto con datos separados por comas |
| **DataFrame** | Una tabla que Spark tiene en memoria para trabajar |
| **Tabla Delta** | Una tabla guardada de forma permanente; aparece en el Catalog |
| **Esquema de datos (`StructType`)** | La lista de columnas con su tipo: número, fecha o texto |
| **Nulo (`null`)** | Una casilla vacía |
| **EDA** | Análisis exploratorio: mirar los datos antes de usarlos |
| **`GROUP BY`** | Agrupar filas iguales para contarlas o sumarlas |
| **Mediana** | El valor del medio cuando ordenas varias medidas de menor a mayor |
| **Calentamiento** | Una primera ejecución que no se cuenta, porque suele ser más lenta |

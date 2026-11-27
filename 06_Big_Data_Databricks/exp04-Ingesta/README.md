# Guía de ejecución · EXP-04 Ingesta: esquema explícito vs inferSchema

Proyecto: Base de Datos Avanzadas y Big Data · Grupo 2 · UPN
Carpeta del repositorio: `06_Big_Data_Databricks/exp04-Ingesta`
Datos: `asistencias_15000.csv` y `tareas_15000.csv` (15 000 filas cada uno, datos sintéticos)

Esta guía te lleva de la mano **desde que entras a Databricks hasta el último resultado**. No necesitas saber programar: solo leer con calma, copiar, pegar y mirar qué sale.

---

## 0. ¿Qué vamos a hacer?

Imagina que llega un camión con 15 000 cajas (filas) y tienes que guardarlas en la bodega. Puedes hacerlo de dos maneras:

- **Con la lista en la mano (esquema explícito):** antes de abrir las cajas ya sabes qué hay en cada una: "esta columna son números, esta son fechas, esta es texto". Solo guardas.
- **Adivinando (`inferSchema`):** abres las cajas, miras qué hay dentro y **adivinas** el tipo. Eso obliga a revisar todo una vez más antes de guardar.

**Ingesta** es justamente eso: el momento en que los datos **entran** al sistema.

**La pregunta del experimento:** ¿Cambia el **tiempo de lectura** y el **tipo de dato** de las columnas si yo le digo a Spark el esquema, en lugar de dejar que lo adivine?

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
4. En **Schema name** (nombre del esquema) escribe: **`exp04_ingesta`**
5. Pulsa **Create** (crear).

> ⚠️ **Reglas para el nombre:** solo letras minúsculas, números y guion bajo `_`.
> **Sin tildes, sin espacios y sin guion medio `-`.** Por ejemplo `analítica` o `particion-ana` darán problemas después (el código necesitaría unas comillas especiales `` ` `` para entenderlos).
> Si el nombre ya existe, agrégale tu nombre: `exp04_ingesta_tunombre`. **Si cambias el nombre, anótalo**: lo usarás en el Paso 8.

---

## 4. Paso 3 · Crear el volumen (la caja)

Un **volumen** es como una **caja dentro del estante** donde se guardan **archivos** (por ejemplo, los CSV). Las tablas van sueltas en el estante; los archivos van en la caja.

1. Dentro del Catalog, haz clic en tu esquema **`exp04_ingesta`**.
2. Arriba a la derecha pulsa **Create** (crear) → **Volume** (volumen).
3. En **Volume name** escribe: **`vol_ingesta`**
4. Deja el tipo en **Managed volume** (volumen administrado: Databricks lo cuida por ti).
5. Pulsa **Create**.

---

## 5. Paso 4 · Crear el directorio (la carpeta)

Un **directorio** es una **carpeta dentro de la caja**, para tener todo ordenado.

1. Haz clic en tu volumen **`vol_ingesta`**.
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
/Volumes/workspace/exp04_ingesta/vol_ingesta/datos/asistencias_15000.csv
```

| Parte de la ruta | Qué es |
|---|---|
| `/Volumes` | La zona de Databricks donde viven los archivos |
| `workspace` | El catálogo (la biblioteca completa) |
| `exp04_ingesta` | Tu esquema (el estante) |
| `vol_ingesta` | Tu volumen (la caja) |
| `datos` | Tu directorio (la carpeta) |
| `asistencias_15000.csv` | El archivo (la hoja) |

> 💡 Si haces clic en un archivo, Databricks muestra un botón para **copiar la ruta**. Es la forma más segura de no equivocarse con una letra.
> Las rutas distinguen **mayúsculas y minúsculas**: `datos` y `Datos` son carpetas distintas.

📸 **Captura 1:** el Catalog mostrando el esquema, el volumen, la carpeta `datos` y los dos CSV.

---

## 7. Paso 6 · Crear el notebook (el cuaderno)

Un **notebook** es un **cuaderno digital**. Está hecho de **celdas**: recuadros donde escribes una orden, la ejecutas y debajo aparece el resultado. Es como un cuaderno de laboratorio donde cada experimento queda anotado con su resultado.

1. En el menú izquierdo pulsa **+ New** (nuevo) → **Notebook**.
2. Arriba, haz clic en el título (dice algo como *Untitled Notebook…*) y cámbialo a: **`EXP04_Ingesta`**
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
# EXP-04 · Ingesta: esquema explícito vs inferSchema
**Objetivo:** comparar el tiempo de lectura y los tipos de dato que resultan al cargar un CSV de 15 000 filas con esquema definido (StructType) frente a inferSchema.
**Configuración:** Databricks Free Edition, compute serverless, esquema exp04_ingesta, 1 calentamiento + 5 repeticiones por variante, una ejecución a la vez.
**Arquitectura:** CSV → Volume (datos) → DataFrame (2 variantes de lectura) → tabla Delta → consulta SQL → gráfico de tiempos.
```

**¿Qué hace?** Es la **portada** del cuaderno: dice qué vamos a investigar. Como empieza con `%md`, Databricks la muestra como texto con formato, no como código.

**¿Qué debe salir?** Un título grande y tres líneas de texto.

📸 **Captura:** la portada (sirve como evidencia del **objetivo** y la **configuración**).
### Celda 2 · Configuración (las direcciones)

```python
# Celda 2 · Configuración: dónde está mi estante y dónde están mis archivos
sch  = "workspace.exp04_ingesta"
base = "/Volumes/workspace/exp04_ingesta/vol_ingesta/datos"
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
### Celda 4 · Variante A: cargar con esquema explícito

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

### Celda 5 · Variante B: dejar que Spark adivine los tipos

```python
# Celda 5 · Variante B: leer con inferSchema y comparar los tipos con la variante A
dfAsistInf  = spark.read.csv(f"{base}/asistencias_15000.csv", header=True, inferSchema=True)
dfTareasInf = spark.read.csv(f"{base}/tareas_15000.csv", header=True, inferSchema=True)
for nombre, a, b in [("asistencias", dfAsistencias, dfAsistInf), ("tareas", dfTareas, dfTareasInf)]:
    print(nombre)
    for (c, ta), (_, tb) in zip(a.dtypes, b.dtypes):
        print(f"  {c:20} explícito={ta:10} inferido={tb:10} {'' if ta == tb else '<-- distinto'}")
```

**¿Qué hace?** Lee **los mismos archivos**, pero esta vez sin darle la lista de tipos: `inferSchema=True` significa "adivina tú". Después pone las dos versiones lado a lado, columna por columna, y marca `<-- distinto` donde Spark adivinó un tipo diferente al que nosotros definimos.

**¿Qué debe salir?** Dos listas (asistencias y tareas) con el tipo de cada columna en las dos variantes. **No sabemos de antemano** si alguna columna cambia: **anota lo que te salga**, porque ese es un resultado del experimento. Si no sale ningún `<-- distinto`, también es un resultado válido: significa que Spark adivinó bien todos los tipos, y la diferencia entre las dos formas queda solo en el **tiempo** y en el **control** (con la lista, tú decides los tipos; adivinando, decide Spark).

📸 **Captura:** esta celda con la comparación.

### Celda 6 · Revisar y limpiar las tareas (EDA)

```python
# Celda 6 · EDA y limpieza de tareas: resumen, vacíos, estados y nombre de columna
from pyspark.sql.functions import col, sum as fsum, when
display(dfTareas.describe())
display(dfTareas.select([fsum(when(col(c).isNull(), 1).otherwise(0)).alias(c) for c in dfTareas.columns]))
display(dfTareas.groupBy("Estado_Tarea").count())
dfTareas = dfTareas.withColumnRenamed("Observaciones", "Observacion")
```

**¿Qué hace?** **EDA** es el *análisis exploratorio de datos*: antes de cocinar, revisamos los ingredientes. Da un resumen, cuenta las **casillas vacías** (*nulos*) de cada columna y cuántas tareas hay por estado. Al final cambia el nombre de una columna (eso es **limpieza**).

**¿Qué debe salir?**
- Vacíos: `Fecha_Inicio` **2 057**, `Fecha_Entrega` **4 848**, `Observaciones` **13 106** y **0** en las demás.
- Estados: **Completada 10 452**, **En Progreso 2 521**, **Asignada 2 027**.

> 💡 Que haya vacíos **es normal**: una tarea "Asignada" todavía no empezó, así que no tiene fecha de inicio. No es un error, es la vida real.

📸 **Captura:** esta celda con sus resultados.

### Celda 7 · Contar tareas por estado (para el primer gráfico)

```python
# Celda 7 · Tareas por estado, lista para graficar
display(dfTareas.groupBy("Estado_Tarea").count().withColumnRenamed("count", "cantidad"))
```

**¿Qué hace?** Cuenta las tareas de cada estado y llama `cantidad` a la columna del conteo.
**¿Qué debe salir?** Una tabla de 3 filas. Sobre ella harás el **Gráfico 1** del Paso 9.

### Celda 8 · Guardar como tablas permanentes

```python
# Celda 8 · Guardar las tablas Delta (variante A, esquema explícito)
dfAsistencias.write.mode("overwrite").saveAsTable(f"{sch}.tb_asistencias")
dfTareas.write.mode("overwrite").saveAsTable(f"{sch}.tb_tareas")
```

**¿Qué hace?** Hasta ahora los datos solo estaban en la **memoria** (como escribir en la pizarra). `saveAsTable` los guarda como **tablas Delta** permanentes en tu estante (como pasarlos al cuaderno). `overwrite` significa "si ya existe, reemplázala".

**¿Qué debe salir?** Nada, solo el ✓. Si vas al Catalog → tu esquema, verás `tb_asistencias` y `tb_tareas`.

📸 **Captura:** el Catalog mostrando las dos tablas.

### Celda 9 · Pregunta con SQL: ¿cuántas tareas hay de cada estado?

```sql
%sql
-- Celda 9 · Contar tareas por estado con COUNT + GROUP BY, de mayor a menor
SELECT Estado_Tarea, COUNT(*) AS cantidad
FROM workspace.exp04_ingesta.tb_tareas
GROUP BY Estado_Tarea
ORDER BY cantidad DESC
```

**¿Qué hace?** **SQL** es un idioma para hacerle preguntas a las tablas. Se lee casi como una frase:
- `SELECT` → "muéstrame el estado y cuántos hay".
- `FROM` → "de la tabla de tareas".
- `GROUP BY` → "agrupando los que tienen el mismo estado" (como separar fichas por color).
- `ORDER BY ... DESC` → "del mayor al menor".

**¿Qué debe salir?** Completada **10452**, En Progreso **2521**, Asignada **2027**.

> ⚠️ Si tu esquema tiene otro nombre, cámbialo en la línea `FROM`. Esta celda **sí** empieza con `%sql`.

📸 **Captura:** esta celda con su resultado.

### Celda 10 · ¡El experimento! Cronometrar las dos formas de leer

```python
# Celda 10 · Medir la lectura (read + count) con y sin esquema: 1 calentamiento + 5 repeticiones
import time, statistics as st, pandas as pd
def medir(fn, n=5):
    fn(); t = []                                    # 1.ª vez = calentamiento (no se cuenta)
    for _ in range(n):
        s = time.perf_counter(); fn(); t.append(time.perf_counter() - s)
    return t
casos = [("asistencias", "explicito",   lambda: spark.read.csv(f"{base}/asistencias_15000.csv", header=True, schema=esq_a).count()),
         ("asistencias", "inferSchema", lambda: spark.read.csv(f"{base}/asistencias_15000.csv", header=True, inferSchema=True).count()),
         ("tareas",      "explicito",   lambda: spark.read.csv(f"{base}/tareas_15000.csv", header=True, schema=esq_t).count()),
         ("tareas",      "inferSchema", lambda: spark.read.csv(f"{base}/tareas_15000.csv", header=True, inferSchema=True).count())]
res = []
for tabla, variante, fn in casos:
    t = medir(fn); res.append((tabla, variante, st.median(t), min(t), max(t)))
dfRes = spark.createDataFrame(pd.DataFrame(res, columns=["tabla", "variante", "mediana_s", "minimo_s", "maximo_s"]))
display(dfRes)
```

**¿Qué hace?** Lee cada archivo de las dos maneras (con lista y adivinando) y cronometra cuánto tarda cada una.

> 💡 **¿Cómo medimos el tiempo?** La función `medir` hace lo que haría un entrenador con un cronómetro:
> 1. Primero hace una **vuelta de calentamiento** que no se cuenta, porque la primera siempre sale más lenta.
> 2. Después repite **5 veces** y anota cuánto tardó cada vez (`time.perf_counter()` es el cronómetro).
> 3. Al final reportamos la **mediana** (el tiempo del medio), el **mínimo** y el **máximo**. Usamos la mediana porque no la arruina una vuelta rara.
>
> **Mientras corre esta celda no ejecutes nada más**, porque eso alteraría el cronómetro.

**¿Qué debe salir?** Una tabla de **4 filas** (asistencias y tareas, cada una con `explicito` e `inferSchema`) con `mediana_s`, `minimo_s` y `maximo_s` en **segundos**. Tarda entre **30 y 90 segundos**. Los segundos exactos **no tienen un valor fijo**: dependen de qué tan ocupado esté el computador.

📸 **Captura:** esta celda con la tabla de tiempos (es el **resultado** principal).

### Celda 11 · Validación: ¿las dos formas leyeron lo mismo?

```python
# Celda 11 · Validación: mismas filas y mismos conteos por estado en las dos variantes
print(dfAsistencias.count(), dfAsistInf.count())
print(dfAsistencias.groupBy("Estado_Asistencia").count().orderBy("Estado_Asistencia").collect() ==
      dfAsistInf.groupBy("Estado_Asistencia").count().orderBy("Estado_Asistencia").collect())
```

**¿Qué hace?** Comprueba que la carrera fue **justa**: que las dos formas leyeron la misma cantidad de filas y los mismos estados. Si no, comparar sus tiempos no tendría sentido.

**¿Qué debe salir?** `15000 15000` y `True` (verdadero). Si sale `False`, **no reportes los tiempos** y avisa al grupo.

📸 **Captura:** esta celda.

### Celda 12 · Preparar la tabla de tipos (para el segundo gráfico)

```python
# Celda 12 · Comparar los tipos de dato entre esquema explícito e inferSchema
filas = []
for tabla, a, b in [("asistencias", dfAsistencias, dfAsistInf), ("tareas", dfTareas, dfTareasInf)]:
    for (c, ta), (_, tb) in zip(a.dtypes, b.dtypes):
        filas.append((tabla, c, ta, tb, ta != tb))
dfTipos = spark.createDataFrame(pd.DataFrame(filas, columns=["tabla", "columna", "tipo_explicito", "tipo_inferido", "distinto"]))
display(dfTipos)
display(dfTipos.groupBy("tabla").agg(fsum(when(col("distinto"), 1).otherwise(0)).alias("columnas_distintas")))
```

**¿Qué hace?** Arma una tabla con cada columna y sus dos tipos, y luego cuenta **cuántas columnas cambiaron** en cada archivo.
**¿Qué debe salir?** Dos tablas. La segunda tiene 2 filas (asistencias y tareas) con `columnas_distintas`. Sobre ella harás el **Gráfico 3**.

> 💡 La celda 6 cambió el nombre `Observaciones` → `Observacion` solo en la variante A. Como comparamos por **posición**, la lista sigue alineada; lo que importa aquí es el **tipo**.

### Valores de control de EXP-04 (si no salen, hay un error)

| Celda | Valor esperado |
|---|---|
| 4 | `Filas cargadas: 15000 15000` |
| 6 | Vacíos: `Fecha_Inicio` 2 057 · `Fecha_Entrega` 4 848 · `Observaciones` 13 106 |
| 6, 7 y 9 | Completada 10 452 · En Progreso 2 521 · Asignada 2 027 |
| 11 | `15000 15000` y `True` |
| 10 | Los segundos **no** tienen un valor fijo: anota los tuyos |
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

### Gráfico 1 · Tareas por estado (sobre la Celda 7)
- X column: `Estado_Tarea` · Y columns: `cantidad`
- Ejes: `Estado de la tarea` y `Cantidad de tareas` · Data labels: activados

```
%md
**Qué demuestra:** cuántas de las 15 000 tareas están completadas, en progreso o asignadas.
Lectura: predominan las tareas completadas (10 452); las asignadas son las que aún no empiezan y por eso no tienen fecha de inicio.
```

### Gráfico 2 · Tiempo de lectura por variante (sobre la Celda 10)
- X column: `tabla` · Y columns: `mediana_s` · **Group by:** `variante` (así salen dos barras por tabla, una por variante)
- Ejes: `Tabla leída` y `Tiempo de lectura (s)` · Data labels con formato `0.000`
- Nombre de la pestaña: `Tiempo de lectura: esquema explícito vs inferSchema`

```
%md
**Qué demuestra:** compara cuánto tarda Spark en leer el mismo CSV de 15 000 filas cuando le damos el esquema frente a cuando lo adivina.
Mediana con esquema explícito: ... s (asistencias) y ... s (tareas). Con inferSchema: ... s y ... s.
Lectura: inferSchema recorre el archivo una vez más para deducir los tipos, por eso se espera que tarde más.
```

### Gráfico 3 · Columnas que cambian de tipo (sobre la 2.ª tabla de la Celda 12)
- X column: `tabla` · Y columns: `columnas_distintas`
- Ejes: `Tabla` y `Columnas con tipo distinto` · Data labels: activados
- Nombre de la pestaña: `Columnas con tipo distinto al inferir el esquema`

```
%md
**Qué demuestra:** cuántas columnas cambian de tipo cuando Spark adivina el esquema en lugar de usar el que definimos.
Columnas distintas: ... en asistencias y ... en tareas.
Lectura: si sale 0, Spark adivinó bien todos los tipos con estos datos; aun así, el esquema explícito garantiza los tipos aunque el archivo cambie. Si sale más de 0, esas columnas necesitarían conversión.
```


---

## 11. Paso 10 · Conclusión, capturas y entrega

### Celda final · Comparación y análisis (celda de texto)

Agrega una celda **+ Text** al final y completa los `...` con **tus** números. No inventes valores: copia los que salieron en tu notebook.

```
%md
## Comparación y análisis
- Variante más rápida por tabla: ...  (mediana en segundos)
- Columnas con tipo distinto entre variantes: ...
- Interpretación: inferSchema hace una lectura extra para deducir los tipos y, según los datos, puede asignar tipos distintos; el esquema explícito evita la lectura extra y fija los tipos.
- Limitaciones: 15 000 filas, datos sintéticos, una sola sesión, compute serverless (no muestra uso de CPU ni RAM).
```

### Lista de capturas

El profesor pide documentar **objetivo, procedimiento y pasos, configuración, resultados, comparación y análisis** y **evidencias de ejecución**. En cada captura debe verse el **✓ verde con la hora**, y en ninguna debe aparecer tu correo.

- [ ] Catalog con esquema, volumen, carpeta `datos` y los 2 CSV (Paso 5)
- [ ] Notebook con su nombre y **Serverless** conectado (Paso 6)
- [ ] Celda 1 · portada
- [ ] Celda 3 · contenido de los archivos
- [ ] Celda 4 · DataFrames y conteo
- [ ] Celda 5 · comparación de tipos
- [ ] Celda 6 · EDA
- [ ] Celda 8 · tablas en el Catalog
- [ ] Celda 9 · consulta `GROUP BY`
- [ ] Celda 10 · tabla de tiempos
- [ ] Celda 11 · validación `True`
- [ ] Gráficos 1, 2 y 3 con su texto de "Qué demuestra"
- [ ] Celda final · comparación y análisis

Guarda las capturas en la carpeta `capturas/` de esta misma carpeta del repositorio. El nombre final de cada captura lo define el grupo al integrar el informe.

### Exportar y entregar
1. **Exportar el notebook:** arriba, **File** (archivo) → **Export** (exportar) → **HTML**. Ese archivo es la evidencia completa de que todo se ejecutó.
2. **Descargar la tabla de resultados:** la de la **Celda 10** (tiempos) y la de la **Celda 12** (tipos). Debajo de la tabla, pulsa el botón de descarga (flecha ⤓) y elige **CSV**. Guárdala en la carpeta `archivos-csv/`.
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

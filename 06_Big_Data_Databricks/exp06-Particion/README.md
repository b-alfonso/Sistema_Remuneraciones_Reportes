# Guía de ejecución · EXP-06 Particionamiento de la tabla Delta

Proyecto: Base de Datos Avanzadas y Big Data · Grupo 2 · UPN
Carpeta del repositorio: `06_Big_Data_Databricks/exp06-Particion`
Datos: `asistencias_15000.csv` y `tareas_15000.csv` (15 000 filas cada uno, datos sintéticos)

Esta guía te lleva de la mano **desde que entras a Databricks hasta el último resultado**. No necesitas saber programar: solo leer con calma, copiar, pegar y mirar qué sale.

---

## 0. ¿Qué vamos a hacer?

Imagina un álbum con 15 000 figuritas. Si te piden "las tardanzas de septiembre", tienes dos opciones:

- **Álbum sin separar:** revisas las 15 000 figuritas una por una.
- **Álbum separado por mes** (julio, agosto, septiembre): vas directo a la sección de septiembre y te saltas el resto.

**Particionar** es eso: guardar la tabla **dividida en partes** según el valor de una columna (por ejemplo, el mes). Así Spark puede leer **solo la parte que necesita**. A eso se le llama *partition pruning* (podar particiones). Pero cuidado: dividir también crea **más archivos**, y con pocos datos eso puede no valer la pena.

**La pregunta del experimento:** ¿Una consulta filtrada es **más rápida** si la tabla está particionada **por mes** o **por estado**, comparada con una tabla **sin partición**?

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
4. En **Schema name** (nombre del esquema) escribe: **`exp06_particion`**
5. Pulsa **Create** (crear).

> ⚠️ **Reglas para el nombre:** solo letras minúsculas, números y guion bajo `_`.
> **Sin tildes, sin espacios y sin guion medio `-`.** Por ejemplo `analítica` o `particion-ana` darán problemas después (el código necesitaría unas comillas especiales `` ` `` para entenderlos).
> Si el nombre ya existe, agrégale tu nombre: `exp06_particion_tunombre`. **Si cambias el nombre, anótalo**: lo usarás en el Paso 8.

---

## 4. Paso 3 · Crear el volumen (la caja)

Un **volumen** es como una **caja dentro del estante** donde se guardan **archivos** (por ejemplo, los CSV). Las tablas van sueltas en el estante; los archivos van en la caja.

1. Dentro del Catalog, haz clic en tu esquema **`exp06_particion`**.
2. Arriba a la derecha pulsa **Create** (crear) → **Volume** (volumen).
3. En **Volume name** escribe: **`vol_particion`**
4. Deja el tipo en **Managed volume** (volumen administrado: Databricks lo cuida por ti).
5. Pulsa **Create**.

---

## 5. Paso 4 · Crear el directorio (la carpeta)

Un **directorio** es una **carpeta dentro de la caja**, para tener todo ordenado.

1. Haz clic en tu volumen **`vol_particion`**.
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
/Volumes/workspace/exp06_particion/vol_particion/datos/asistencias_15000.csv
```

| Parte de la ruta | Qué es |
|---|---|
| `/Volumes` | La zona de Databricks donde viven los archivos |
| `workspace` | El catálogo (la biblioteca completa) |
| `exp06_particion` | Tu esquema (el estante) |
| `vol_particion` | Tu volumen (la caja) |
| `datos` | Tu directorio (la carpeta) |
| `asistencias_15000.csv` | El archivo (la hoja) |

> 💡 Si haces clic en un archivo, Databricks muestra un botón para **copiar la ruta**. Es la forma más segura de no equivocarse con una letra.
> Las rutas distinguen **mayúsculas y minúsculas**: `datos` y `Datos` son carpetas distintas.

📸 **Captura 1:** el Catalog mostrando el esquema, el volumen, la carpeta `datos` y los dos CSV.

---

## 7. Paso 6 · Crear el notebook (el cuaderno)

Un **notebook** es un **cuaderno digital**. Está hecho de **celdas**: recuadros donde escribes una orden, la ejecutas y debajo aparece el resultado. Es como un cuaderno de laboratorio donde cada experimento queda anotado con su resultado.

1. En el menú izquierdo pulsa **+ New** (nuevo) → **Notebook**.
2. Arriba, haz clic en el título (dice algo como *Untitled Notebook…*) y cámbialo a: **`EXP06_Particionamiento`**
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
# EXP-06 · Particionamiento de la tabla Delta
**Objetivo:** comparar la latencia de una consulta filtrada sobre asistencias (15 000 filas) en una tabla sin partición, particionada por mes y particionada por estado.
**Configuración:** Databricks Free Edition, compute serverless, esquema exp06_particion, 1 calentamiento + 5 repeticiones por tabla, una ejecución a la vez.
**Arquitectura:** CSV → Volume (datos) → DataFrame de Spark → 3 tablas Delta → consulta SQL → gráfico de tiempos.
```

**¿Qué hace?** Es la **portada** del cuaderno: dice qué vamos a investigar. Como empieza con `%md`, Databricks la muestra como texto con formato, no como código.

**¿Qué debe salir?** Un título grande y tres líneas de texto.

📸 **Captura:** la portada (sirve como evidencia del **objetivo** y la **configuración**).
### Celda 2 · Configuración (las direcciones)

```python
# Celda 2 · Configuración: dónde está mi estante y dónde están mis archivos
sch  = "workspace.exp06_particion"
base = "/Volumes/workspace/exp06_particion/vol_particion/datos"
```

**¿Qué hace?** Guarda en **variables** las direcciones que usaremos todo el tiempo. Una variable es como una **cajita con nombre**: en `sch` guardamos el nombre del estante y en `base` la dirección de la carpeta de los CSV. Así no escribimos la dirección larga en cada celda.

**¿Qué debe salir?** Nada, solo el ✓ verde. Es normal.

> ⚠️ Si en los Pasos 2, 3 o 4 usaste otros nombres, **cámbialos aquí**, dentro de las comillas.
### Celda 3 · Mirar el archivo por dentro

```python
# Celda 3 · Mostrar las primeras líneas del CSV de asistencias
print(dbutils.fs.head(f"{base}/asistencias_15000.csv", 600))
```

**¿Qué hace?** Abre el archivo y muestra solo el **comienzo**, como cuando hojeas la primera página de un libro. `print` significa "muéstralo en pantalla".

**¿Qué debe salir?** La fila de títulos `ID_Asistencia,ID_Trabajador,Fecha_Entrada,Fecha_Salida,Fecha_Calculada,Estado_Asistencia` y filas como `1,1,2026-07-01 08:59:00,2026-07-01 18:00:00,2026-07-01,A tiempo`.

> 💡 En clase se usaba `%fs head`. El computador Serverless no lo acepta, por eso usamos `dbutils.fs.head`, que hace lo mismo.

📸 **Captura:** esta celda con su resultado.
### Celda 4 · Cargar los datos en un DataFrame

```python
# Celda 4 · Cargar el CSV en un DataFrame con su esquema (lista de columnas y tipos)
from pyspark.sql.types import *
esquema_asist = StructType([
    StructField("ID_Asistencia", IntegerType()), StructField("ID_Trabajador", IntegerType()),
    StructField("Fecha_Entrada", TimestampType()), StructField("Fecha_Salida", TimestampType()),
    StructField("Fecha_Calculada", DateType()), StructField("Estado_Asistencia", StringType())])
dfAsistencias = spark.read.csv(f"{base}/asistencias_15000.csv", header=True, schema=esquema_asist)
print("Filas cargadas:", dfAsistencias.count())
display(dfAsistencias)
```

**¿Qué hace?**
- Primero escribe el **esquema de datos**: una lista que dice qué tipo de dato tiene cada columna. Es como poner etiquetas en los cajones: **números** (`IntegerType`), **fecha y hora** (`TimestampType`), **fecha** (`DateType`) y **texto** (`StringType`).
- Luego lee el CSV y lo convierte en un **DataFrame**: una tabla que Spark tiene en memoria, lista para trabajar.
- `header=True` le avisa que la primera fila son los **títulos**. `count()` cuenta filas y `display()` muestra la tabla.

**¿Qué debe salir?** `Filas cargadas: 15000` y una tabla de 6 columnas.

📸 **Captura:** esta celda con el conteo y la tabla.
### Celda 5 · Revisar y limpiar los datos (EDA)

```python
# Celda 5 · EDA y limpieza: resumen, vacíos, estados, horas coherentes y nombre de columna
from pyspark.sql.functions import col, sum as fsum, when
display(dfAsistencias.describe())
display(dfAsistencias.select([fsum(when(col(c).isNull(), 1).otherwise(0)).alias(c) for c in dfAsistencias.columns]))
display(dfAsistencias.groupBy("Estado_Asistencia").count())
print("Salida antes de entrada:", dfAsistencias.filter(col("Fecha_Salida") < col("Fecha_Entrada")).count())
dfAsistencias = dfAsistencias.dropna().withColumnRenamed("Fecha_Calculada", "fecha")
print("Filas tras la limpieza:", dfAsistencias.count())
```

**¿Qué hace?** **EDA** significa *análisis exploratorio de datos*: antes de cocinar, revisamos que los ingredientes estén buenos.
1. `describe()` da un resumen: cuántos hay, el mínimo y el máximo.
2. La segunda línea cuenta las **casillas vacías** (*nulos*) de cada columna.
3. `groupBy(...).count()` cuenta cuántas asistencias hay de cada estado.
4. Revisa que nadie haya **salido antes de entrar** (eso sería un error en los datos).
5. `dropna()` quita filas con casillas vacías y `withColumnRenamed` le cambia el nombre `Fecha_Calculada` por uno más corto: `fecha`.

**¿Qué debe salir?**
- Resumen con `count = 15000`.
- Vacíos: **0** en todas las columnas.
- Estados: **A tiempo 13 869** y **Tardanza 1 131**.
- `Salida antes de entrada: 0`
- `Filas tras la limpieza: 15000`. No se borró nada porque los datos estaban completos.

📸 **Captura:** esta celda con sus resultados.

### Celda 6 · Crear la columna `mes` y contar por estado

```python
# Celda 6 · Crear la columna mes (la usaremos para particionar) y contar asistencias por estado
from pyspark.sql.functions import month
dfAsistencias = dfAsistencias.withColumn("mes", month("fecha"))
display(dfAsistencias.groupBy("Estado_Asistencia").count().withColumnRenamed("count", "cantidad"))
```

**¿Qué hace?** `withColumn` agrega una **columna nueva** llamada `mes`. `month("fecha")` saca el número del mes de cada fecha: julio = 7, agosto = 8, septiembre = 9. Es como escribir en cada figurita a qué mes pertenece, para poder separarlas después.

**¿Qué debe salir?** Dos filas: A tiempo **13 869** y Tardanza **1 131**. Sobre ella harás el **Gráfico 1**.

### Celda 7 · Guardar la tabla SIN partición (la de referencia)

```python
# Celda 7 · Guardar la tabla Delta sin partición (variante de referencia)
dfAsistencias.write.mode("overwrite").saveAsTable(f"{sch}.tb_asist_sin_particion")
```

**¿Qué hace?** Pasa los datos de la **memoria** (la pizarra) a una **tabla Delta** permanente (el cuaderno). Esta es el **álbum sin separar**: la usaremos para comparar.
**¿Qué debe salir?** Solo el ✓. En el Catalog aparece `tb_asist_sin_particion`.

### Celda 8 · Pregunta con SQL: ¿cuántas asistencias hay de cada estado?

```sql
%sql
-- Celda 8 · Contar asistencias por estado con COUNT + GROUP BY, de mayor a menor
SELECT Estado_Asistencia, COUNT(*) AS cantidad
FROM workspace.exp06_particion.tb_asist_sin_particion
GROUP BY Estado_Asistencia
ORDER BY cantidad DESC
```

**¿Qué hace?** **SQL** es un idioma para preguntarle cosas a las tablas: `SELECT` (muéstrame), `FROM` (de esta tabla), `GROUP BY` (agrupando los iguales, como separar fichas por color) y `ORDER BY ... DESC` (del mayor al menor).
**¿Qué debe salir?** A tiempo **13869** y Tardanza **1131**.

> ⚠️ Esta celda **sí** empieza con `%sql`. Si tu esquema tiene otro nombre, cámbialo en `FROM`. Si el nombre lleva guion medio, escríbelo entre comillas invertidas: `` workspace.`exp06_particion-nombre`.tb_asist_sin_particion ``.

📸 **Captura:** esta celda.

### Celda 9 · Crear las dos tablas particionadas

```python
# Celda 9 · Crear las dos tablas Delta particionadas: una por mes y otra por estado
dfAsistencias.write.mode("overwrite").partitionBy("mes").saveAsTable(f"{sch}.tb_asist_part_mes")
dfAsistencias.write.mode("overwrite").partitionBy("Estado_Asistencia").saveAsTable(f"{sch}.tb_asist_part_estado")
```

**¿Qué hace?** Guarda **los mismos datos** dos veces más, pero ahora **separados**: `partitionBy("mes")` hace un "cajón" por cada mes y `partitionBy("Estado_Asistencia")` hace un cajón para "A tiempo" y otro para "Tardanza".
**¿Qué debe salir?** Solo el ✓. En el Catalog aparecen `tb_asist_part_mes` y `tb_asist_part_estado`.

📸 **Captura:** el Catalog con las **tres** tablas.

### Celda 10 · ¿Cuántos archivos y cuánto pesa cada tabla?

```python
# Celda 10 · Comparar cantidad de archivos y tamaño de cada tabla
for t in ["tb_asist_sin_particion", "tb_asist_part_mes", "tb_asist_part_estado"]:
    display(spark.sql(f"DESCRIBE DETAIL {sch}.{t}").select("name", "numFiles", "sizeInBytes"))
```

**¿Qué hace?** `DESCRIBE DETAIL` es como leer la **ficha técnica** de cada tabla. Mostramos `numFiles` (cuántos archivos tiene) y `sizeInBytes` (cuánto pesa en bytes).

**¿Qué debe salir?** Tres tablitas. Lo esperable: la tabla sin partición con **pocos archivos**, la de mes con **al menos 3** (julio, agosto y septiembre) y la de estado con **al menos 2**. **Anota los valores exactos.**

📸 **Captura:** esta celda.

### Celda 11 · ¡El experimento! Cronometrar la misma pregunta en las 3 tablas

```python
# Celda 11 · Medir la consulta filtrada en cada tabla (1 calentamiento + 5 repeticiones)
import time, statistics as st, pandas as pd
def medir(fn, n=5):
    fn(); t = []                                    # 1.ª vez = calentamiento (no se cuenta)
    for _ in range(n):
        s = time.perf_counter(); fn(); t.append(time.perf_counter() - s)
    return t
res = []
for t in ["tb_asist_sin_particion", "tb_asist_part_mes", "tb_asist_part_estado"]:
    q = f"SELECT COUNT(*) FROM {sch}.{t} WHERE mes = 9 AND Estado_Asistencia = 'Tardanza'"
    tiempos = medir(lambda: spark.sql(q).collect())
    print(t, "->", spark.sql(q).collect()[0][0], "filas")
    res.append((t, st.median(tiempos), min(tiempos), max(tiempos)))
dfRes = spark.createDataFrame(pd.DataFrame(res, columns=["tabla", "mediana_s", "minimo_s", "maximo_s"]))
display(dfRes)
```

**¿Qué hace?** Le hace **la misma pregunta** a las tres tablas: "¿cuántas tardanzas hubo en septiembre?" (`WHERE` significa "solo las que cumplan esto"), y cronometra cuánto tarda cada una.

> 💡 **¿Cómo medimos el tiempo?** La función `medir` hace lo que haría un entrenador con un cronómetro:
> 1. Primero hace una **vuelta de calentamiento** que no se cuenta, porque la primera siempre sale más lenta.
> 2. Después repite **5 veces** y anota cuánto tardó cada vez (`time.perf_counter()` es el cronómetro).
> 3. Al final reportamos la **mediana** (el tiempo del medio), el **mínimo** y el **máximo**. Usamos la mediana porque no la arruina una vuelta rara.
>
> **Mientras corre esta celda no ejecutes nada más**, porque eso alteraría el cronómetro.

**¿Qué debe salir?**
- Tres líneas que dicen **`383 filas`** cada una. Si alguna da otro número, hay un error.
- Una tabla de **3 filas** con `mediana_s`, `minimo_s` y `maximo_s`. Tarda de **10 a 40 segundos**. Los segundos **no tienen un valor fijo**.

📸 **Captura:** esta celda con las 383 filas y la tabla de tiempos (es el **resultado** principal).

### Celda 12 · Resumen de archivos (para el último gráfico)

```python
# Celda 12 · Juntar archivos y tamaño de las 3 tablas en una sola tabla para graficar
filas = []
for t in ["tb_asist_sin_particion", "tb_asist_part_mes", "tb_asist_part_estado"]:
    d = spark.sql(f"DESCRIBE DETAIL {sch}.{t}").select("numFiles", "sizeInBytes").collect()[0]
    filas.append((t, d.numFiles, d.sizeInBytes))
display(spark.createDataFrame(filas, ["tabla", "numFiles", "sizeInBytes"]))
```

**¿Qué hace?** Junta en **una sola tabla** lo que la Celda 10 mostró por separado.
**¿Qué debe salir?** Una tabla de 3 filas. Sobre ella harás el **Gráfico 3**.

### Valores de control de EXP-06 (si no salen, hay un error)

| Celda | Valor esperado |
|---|---|
| 4 | `Filas cargadas: 15000` |
| 5 | Vacíos 0 · A tiempo 13 869 · Tardanza 1 131 · `Salida antes de entrada: 0` · `Filas tras la limpieza: 15000` |
| 8 | A tiempo 13869 · Tardanza 1131 |
| 11 | Las tres tablas: **383 filas** |
| 10, 11 y 12 | Archivos, bytes y segundos **no** tienen un valor fijo: anota los tuyos |
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

### Gráfico 1 · Asistencias por estado (sobre la Celda 6)
- X column: `Estado_Asistencia` · Y columns: `cantidad` · Data labels: activados

```
%md
**Qué demuestra:** cuántas de las 15 000 asistencias fueron a tiempo y cuántas con tardanza.
Lectura: predominan las asistencias a tiempo (13 869 frente a 1 131 tardanzas).
```

### Gráfico 2 · Velocidad de la consulta por tabla (sobre la Celda 11)
- X column: `tabla` · Y columns: `mediana_s`, `minimo_s` y `maximo_s` (sin apilar: *Stacking* desactivado)
- Ejes: `Tabla Delta` y `Tiempo de consulta (s)` · Data labels `0.000`
- En la pestaña **Series** renombra las barras como `Mediana`, `Mínimo` y `Máximo`
- Nombre de la pestaña: `Latencia de la consulta filtrada por tabla`

```
%md
**Qué demuestra:** cuánto tarda en contar las tardanzas de septiembre (383 filas) la tabla sin partición, la particionada por mes y la particionada por estado.
Mediana: sin partición ... s · por mes ... s · por estado ... s.
Lectura: si la diferencia es menor que la variación entre repeticiones y los rangos mínimo–máximo se cruzan, con 15 000 filas no se puede afirmar que el particionamiento mejore la consulta.
```

### Gráfico 3 · Archivos por tabla (sobre la Celda 12)
- X column: `tabla` · Y columns: `numFiles` · Ejes: `Tabla Delta` y `Cantidad de archivos` · Data labels: activados
- Nombre de la pestaña: `Archivos por tabla`

```
%md
**Qué demuestra:** cuántos archivos genera cada forma de guardar la misma tabla.
Archivos: sin partición ... · por mes ... · por estado ...
Lectura: particionar divide la tabla en más archivos pequeños; con pocos datos eso agrega trabajo y puede no compensar.
```


---

## 11. Paso 10 · Conclusión, capturas y entrega

### Celda final · Comparación y análisis (celda de texto)

Agrega una celda **+ Text** al final y completa los `...` con **tus** números. No inventes valores: copia los que salieron en tu notebook.

```
%md
## Comparación y análisis
- Tabla más rápida (mediana): ...  (segundos)
- Las tres consultas devolvieron 383 filas, así que son comparables.
- Archivos generados: sin partición ...; por mes ...; por estado ...
- Interpretación: con 15 000 filas el particionamiento crea más archivos pequeños y puede no mejorar la consulta; el tiempo parece dominado por costos fijos de cada consulta.
- Limitaciones: datos sintéticos, 5 repeticiones, una sola sesión, compute serverless (no muestra uso de CPU ni RAM).
```

### Lista de capturas

El profesor pide documentar **objetivo, procedimiento y pasos, configuración, resultados, comparación y análisis** y **evidencias de ejecución**. En cada captura debe verse el **✓ verde con la hora**, y en ninguna debe aparecer tu correo.

- [ ] Catalog con esquema, volumen, carpeta `datos` y los 2 CSV (Paso 5)
- [ ] Notebook con su nombre y **Serverless** conectado (Paso 6)
- [ ] Celda 1 · portada
- [ ] Celda 3 · contenido del archivo
- [ ] Celda 4 · DataFrame y conteo
- [ ] Celda 5 · EDA
- [ ] Celda 8 · consulta `GROUP BY`
- [ ] Catalog con las 3 tablas
- [ ] Celda 10 · archivos y tamaño
- [ ] Celda 11 · 383 filas y tabla de tiempos
- [ ] Gráficos 1, 2 y 3 con su texto de "Qué demuestra"
- [ ] Celda final · comparación y análisis

Guarda las capturas en la carpeta `capturas/` de esta misma carpeta del repositorio. El nombre final de cada captura lo define el grupo al integrar el informe.

### Exportar y entregar
1. **Exportar el notebook:** arriba, **File** (archivo) → **Export** (exportar) → **HTML**. Ese archivo es la evidencia completa de que todo se ejecutó.
2. **Descargar la tabla de resultados:** la de la **Celda 11** (tiempos) y la de la **Celda 12** (archivos). Debajo de la tabla, pulsa el botón de descarga (flecha ⤓) y elige **CSV**. Guárdala en la carpeta `archivos-csv/`.
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

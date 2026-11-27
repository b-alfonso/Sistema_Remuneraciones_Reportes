# Guía de ejecución · EXP-05 Formato de almacenamiento: CSV vs Parquet vs Delta

Proyecto: Base de Datos Avanzadas y Big Data · Grupo 2 · UPN
Carpeta del repositorio: `06_Big_Data_Databricks/exp05-Formatos`
Datos: `asistencias_15000.csv` y `tareas_15000.csv` (15 000 filas cada uno, datos sintéticos)

Esta guía te lleva de la mano **desde que entras a Databricks hasta el último resultado**. No necesitas saber programar: solo leer con calma, copiar, pegar y mirar qué sale.

---

## 0. ¿Qué vamos a hacer?

Imagina que tienes que guardar el mismo cuento de tres maneras:

- **CSV:** escrito a mano, letra por letra, en hojas sueltas. Cualquiera lo lee, pero ocupa mucho espacio.
- **Parquet:** el mismo cuento, pero **comprimido y ordenado por columnas**, como un archivador con un cajón para cada tipo de dato. Ocupa mucho menos y se encuentra rápido lo que buscas.
- **Delta:** un archivador Parquet que además tiene un **cuaderno de registro** (`_delta_log`) donde anota cada cambio, como un diario. Así se puede saber qué pasó y volver atrás.

Un **formato de almacenamiento** es la forma en que los datos se guardan en el disco.

**La pregunta del experimento:** Si guardo **las mismas** 15 000 asistencias en CSV, Parquet y Delta, ¿cuál **ocupa menos espacio**, cuál **se escribe más rápido** y cuál **se consulta más rápido**?

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
4. En **Schema name** (nombre del esquema) escribe: **`exp05_formatos`**
5. Pulsa **Create** (crear).

> ⚠️ **Reglas para el nombre:** solo letras minúsculas, números y guion bajo `_`.
> **Sin tildes, sin espacios y sin guion medio `-`.** Por ejemplo `analítica` o `particion-ana` darán problemas después (el código necesitaría unas comillas especiales `` ` `` para entenderlos).
> Si el nombre ya existe, agrégale tu nombre: `exp05_formatos_tunombre`. **Si cambias el nombre, anótalo**: lo usarás en el Paso 8.

---

## 4. Paso 3 · Crear el volumen (la caja)

Un **volumen** es como una **caja dentro del estante** donde se guardan **archivos** (por ejemplo, los CSV). Las tablas van sueltas en el estante; los archivos van en la caja.

1. Dentro del Catalog, haz clic en tu esquema **`exp05_formatos`**.
2. Arriba a la derecha pulsa **Create** (crear) → **Volume** (volumen).
3. En **Volume name** escribe: **`vol_formatos`**
4. Deja el tipo en **Managed volume** (volumen administrado: Databricks lo cuida por ti).
5. Pulsa **Create**.

---

## 5. Paso 4 · Crear el directorio (la carpeta)

Un **directorio** es una **carpeta dentro de la caja**, para tener todo ordenado.

1. Haz clic en tu volumen **`vol_formatos`**.
2. Pulsa **Create directory** (crear directorio). Si no lo ves, búscalo en el menú **⋮** (tres puntos).
3. Escribe: **`datos`** y pulsa **Create**.
4. **Repite** y crea un segundo directorio llamado **`salida`**. Ahí Spark guardará los datos en los tres formatos. Al final tu caja tendrá dos carpetas: `datos` (lo que subes tú) y `salida` (lo que crea Spark).

---

## 6. Paso 5 · Subir los dos CSV

1. Entra a la carpeta **`datos`** (haz clic en ella).
2. Pulsa **Upload to this volume** (subir a este volumen).
3. Arrastra `asistencias_15000.csv` y `tareas_15000.csv` al recuadro (o pulsa **Browse** para buscarlos).
4. Pulsa **Upload** (subir) y espera a que terminen.
5. Comprueba que aparecen los dos, con tamaño aproximado de **1 MB** cada uno.

**¿Dónde quedaron?** Cada archivo ahora tiene una **ruta**, que es como su dirección postal:

```
/Volumes/workspace/exp05_formatos/vol_formatos/datos/asistencias_15000.csv
```

| Parte de la ruta | Qué es |
|---|---|
| `/Volumes` | La zona de Databricks donde viven los archivos |
| `workspace` | El catálogo (la biblioteca completa) |
| `exp05_formatos` | Tu esquema (el estante) |
| `vol_formatos` | Tu volumen (la caja) |
| `datos` | Tu directorio (la carpeta) |
| `asistencias_15000.csv` | El archivo (la hoja) |

> 💡 Si haces clic en un archivo, Databricks muestra un botón para **copiar la ruta**. Es la forma más segura de no equivocarse con una letra.
> Las rutas distinguen **mayúsculas y minúsculas**: `datos` y `Datos` son carpetas distintas.

📸 **Captura 1:** el Catalog mostrando el esquema, el volumen, la carpeta `datos` y los dos CSV.

---

## 7. Paso 6 · Crear el notebook (el cuaderno)

Un **notebook** es un **cuaderno digital**. Está hecho de **celdas**: recuadros donde escribes una orden, la ejecutas y debajo aparece el resultado. Es como un cuaderno de laboratorio donde cada experimento queda anotado con su resultado.

1. En el menú izquierdo pulsa **+ New** (nuevo) → **Notebook**.
2. Arriba, haz clic en el título (dice algo como *Untitled Notebook…*) y cámbialo a: **`EXP05_Formatos`**
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
# EXP-05 · Formato de almacenamiento: CSV vs Parquet vs Delta
**Objetivo:** comparar el tamaño en disco, el tiempo de escritura y la latencia de una consulta agrupada cuando las asistencias (15 000 filas) se guardan en CSV, Parquet y Delta.
**Configuración:** Databricks Free Edition, compute serverless, esquema exp05_formatos, 1 calentamiento + 5 repeticiones por formato, una ejecución a la vez.
**Arquitectura:** CSV → Volume (datos) → DataFrame → escritura en 3 formatos (carpeta salida) → lectura y consulta GROUP BY → gráficos de tamaño y tiempo.
```

**¿Qué hace?** Es la **portada** del cuaderno: dice qué vamos a investigar. Como empieza con `%md`, Databricks la muestra como texto con formato, no como código.

**¿Qué debe salir?** Un título grande y tres líneas de texto.

📸 **Captura:** la portada (sirve como evidencia del **objetivo** y la **configuración**).
### Celda 2 · Configuración (las direcciones)

```python
# Celda 2 · Configuración: estante, caja, carpeta de datos y carpeta de salida
sch  = "workspace.exp05_formatos"
vol  = "/Volumes/workspace/exp05_formatos/vol_formatos"   # termina en el NOMBRE DE LA CAJA, sin barra final
base = f"{vol}/datos"                                     # aquí están los CSV que subiste
out  = f"{vol}/salida"                                    # aquí Spark guardará los 3 formatos
```

**¿Qué hace?** Guarda en **variables** (cajitas con nombre) las direcciones que usaremos. `vol` es la dirección de la caja; `base` y `out` le **agregan** la carpeta. La `f` antes de las comillas permite meter una variable dentro del texto usando `{ }`.

**¿Qué debe salir?** Nada, solo el ✓ verde.

> ⚠️ **Error muy común:** poner la carpeta dentro de `vol` **y** otra vez en `base`. Eso crea rutas como `.../datos/datos/...` que no existen. `vol` siempre termina en el **volumen**.
> Si tus nombres son otros (por ejemplo tu carpeta se llama `FORMATOS`), cámbialos aquí respetando mayúsculas.

### Celda 3 · Comprobar que la dirección es correcta

```python
# Celda 3 · Comprobación: listar lo que hay en la carpeta de datos
display(dbutils.fs.ls(base))
```

**¿Qué hace?** `ls` significa *listar*: muestra qué archivos hay en esa carpeta. Es como tocar la puerta para ver si alguien contesta.
**¿Qué debe salir?** Una tabla con `asistencias_15000.csv` y `tareas_15000.csv`. Si sale un error, la dirección de la Celda 2 está mal: revísala antes de seguir.
### Celda 4 · Mirar el archivo por dentro

```python
# Celda 4 · Mostrar las primeras líneas del CSV de asistencias
print(dbutils.fs.head(f"{base}/asistencias_15000.csv", 600))
```

**¿Qué hace?** Abre el archivo y muestra solo el **comienzo**, como cuando hojeas la primera página de un libro. `print` significa "muéstralo en pantalla".

**¿Qué debe salir?** La fila de títulos `ID_Asistencia,ID_Trabajador,Fecha_Entrada,Fecha_Salida,Fecha_Calculada,Estado_Asistencia` y filas como `1,1,2026-07-01 08:59:00,2026-07-01 18:00:00,2026-07-01,A tiempo`.

> 💡 En clase se usaba `%fs head`. El computador Serverless no lo acepta, por eso usamos `dbutils.fs.head`, que hace lo mismo.

📸 **Captura:** esta celda con su resultado.
### Celda 5 · Cargar los datos en un DataFrame

```python
# Celda 5 · Cargar el CSV en un DataFrame con su esquema (lista de columnas y tipos)
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
### Celda 6 · Revisar y limpiar los datos (EDA)

```python
# Celda 6 · EDA y limpieza: resumen, vacíos, estados, horas coherentes y nombre de columna
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

### Celda 7 · Contar asistencias por estado (para un gráfico)

```python
# Celda 7 · Asistencias por estado, lista para graficar
display(dfAsistencias.groupBy("Estado_Asistencia").count().withColumnRenamed("count", "cantidad"))
```

**¿Qué debe salir?** Dos filas: A tiempo **13 869** y Tardanza **1 131**. Sobre ella harás el **Gráfico 1**.

### Celda 8 · Guardar como tabla permanente

```python
# Celda 8 · Guardar la tabla Delta en el esquema
dfAsistencias.write.mode("overwrite").saveAsTable(f"{sch}.tb_asistencias")
```

**¿Qué hace?** Pasa los datos de la **memoria** (la pizarra) a una **tabla Delta** permanente (el cuaderno). `overwrite` = "si ya existe, reemplázala".
**¿Qué debe salir?** Solo el ✓. En el Catalog aparece `tb_asistencias`.

📸 **Captura:** el Catalog con la tabla.

### Celda 9 · Pregunta con SQL: ¿cuántas asistencias hay de cada estado?

```sql
%sql
-- Celda 9 · Contar asistencias por estado con COUNT + GROUP BY, de mayor a menor
SELECT Estado_Asistencia, COUNT(*) AS cantidad
FROM workspace.exp05_formatos.tb_asistencias
GROUP BY Estado_Asistencia
ORDER BY cantidad DESC
```

**¿Qué hace?** **SQL** es un idioma para preguntarle cosas a las tablas: `SELECT` (muéstrame), `FROM` (de esta tabla), `GROUP BY` (agrupando los iguales, como separar fichas por color) y `ORDER BY ... DESC` (del mayor al menor).
**¿Qué debe salir?** A tiempo **13869** y Tardanza **1131**.

> ⚠️ Esta celda **sí** empieza con `%sql`. Si tu esquema tiene otro nombre, cámbialo en `FROM`.

📸 **Captura:** esta celda.

### Celda 10 · ¡El experimento, parte 1! Escribir en 3 formatos y cronometrar

```python
# Celda 10 · Escribir el mismo DataFrame en CSV, Parquet y Delta y medir la escritura (1 calentamiento + 5)
import time, statistics as st, pandas as pd
def medir(fn, n=5):
    fn(); t = []                                    # 1.ª vez = calentamiento (no se cuenta)
    for _ in range(n):
        s = time.perf_counter(); fn(); t.append(time.perf_counter() - s)
    return t
rutas = {f: f"{out}/asist_{f}" for f in ["csv", "parquet", "delta"]}
def escribir(f):
    w = dfAsistencias.write.mode("overwrite").format(f)
    (w.option("header", True) if f == "csv" else w).save(rutas[f])
t_escritura = {f: medir(lambda f=f: escribir(f)) for f in rutas}
for f, t in t_escritura.items():
    print(f, "mediana de escritura (s):", round(st.median(t), 3))
```

**¿Qué hace?** Guarda **los mismos datos** tres veces, una en cada formato, dentro de la carpeta `salida`, y cronometra cuánto tarda cada uno.

> 💡 **¿Cómo medimos el tiempo?** La función `medir` hace lo que haría un entrenador con un cronómetro:
> 1. Primero hace una **vuelta de calentamiento** que no se cuenta, porque la primera siempre sale más lenta.
> 2. Después repite **5 veces** y anota cuánto tardó cada vez (`time.perf_counter()` es el cronómetro).
> 3. Al final reportamos la **mediana** (el tiempo del medio), el **mínimo** y el **máximo**. Usamos la mediana porque no la arruina una vuelta rara.
>
> **Mientras corre esta celda no ejecutes nada más**, porque eso alteraría el cronómetro.

**¿Qué debe salir?** Tres líneas (`csv`, `parquet`, `delta`) con su mediana de escritura en segundos. Tarda de **1 a 3 minutos**. En el Catalog, dentro de `salida`, aparecerán tres carpetas: `asist_csv`, `asist_parquet` y `asist_delta`.

> ⚠️ Esta celda es **Python**: **no** debe empezar con `%sql`. Si la pegaste debajo de una celda SQL, revisa la primera línea.

📸 **Captura:** esta celda con sus resultados.

### Celda 11 · ¿Cuánto pesa cada formato?

```python
# Celda 11 · Sumar los bytes y contar los archivos de cada formato (incluye _delta_log en Delta)
def tamano(p):
    total, n = 0, 0
    for x in dbutils.fs.ls(p):
        if x.path.endswith("/"):
            b, c = tamano(x.path); total += b; n += c
        else:
            total += x.size; n += 1
    return total, n
tam = {f: tamano(r) for f, r in rutas.items()}
for f, (b, n) in tam.items():
    print(f, b, "bytes en", n, "archivos")
```

**¿Qué hace?** Entra a cada carpeta (y a sus subcarpetas) y **suma el peso** de todos los archivos, como pesar cada mochila con todo lo que tiene dentro. Un **byte** es la unidad más pequeña de peso digital (1 MB ≈ 1 000 000 bytes).

**¿Qué debe salir?** Tres líneas con bytes y cantidad de archivos. Se espera que el CSV sea **el más pesado** (es texto plano) y que Parquet y Delta pesen **mucho menos** (están comprimidos). Delta tiene más archivos porque incluye su cuaderno de registro `_delta_log`. **Anota tus valores exactos.**

📸 **Captura:** esta celda.

### Celda 12 · ¡El experimento, parte 2! ¿Qué formato se consulta más rápido?

```python
# Celda 12 · Medir lectura + GROUP BY por estado en cada formato (1 calentamiento + 5 repeticiones)
def consulta(f):
    lector = spark.read.format(f)
    lector = lector.option("header", True) if f == "csv" else lector
    return lector.load(rutas[f]).groupBy("Estado_Asistencia").count().collect()
t_consulta = {f: medir(lambda f=f: consulta(f)) for f in rutas}
filas = [(f, tam[f][0], tam[f][1], st.median(t_escritura[f]), st.median(t_consulta[f]), min(t_consulta[f]), max(t_consulta[f])) for f in rutas]
dfRes = spark.createDataFrame(pd.DataFrame(filas, columns=["formato", "bytes", "archivos", "escritura_mediana_s", "consulta_mediana_s", "consulta_minimo_s", "consulta_maximo_s"]))
display(dfRes)
```

**¿Qué hace?** Abre cada formato, cuenta las asistencias por estado y cronometra cuánto demora. Al final junta **todo** (peso, archivos, escritura y consulta) en una sola tabla de resultados.

**¿Qué debe salir?** Una tabla de **3 filas** (`csv`, `parquet`, `delta`). Sobre ella harás los Gráficos 2, 3 y 4.

> 💡 Ojo: el CSV se lee **sin esquema**, así que todas sus columnas quedan como texto. La consulta solo usa `Estado_Asistencia`, que de todas formas es texto, así que la comparación es justa. Menciónalo en tu análisis.

📸 **Captura:** esta celda con la tabla (es el **resultado** principal).

### Celda 13 · Validación: ¿los tres formatos guardaron lo mismo?

```python
# Celda 13 · Validación: los tres formatos deben dar los mismos conteos por estado
for f in rutas:
    lector = spark.read.format(f)
    lector = lector.option("header", True) if f == "csv" else lector
    print(f, sorted([(r[0], r[1]) for r in lector.load(rutas[f]).groupBy("Estado_Asistencia").count().collect()]))
```

**¿Qué hace?** Comprueba que los tres formatos tienen **exactamente los mismos datos**. Si no, la comparación no valdría.
**¿Qué debe salir?** Las tres líneas con `[('A tiempo', 13869), ('Tardanza', 1131)]`. Si alguna es distinta, **no reportes los tiempos** y avisa al grupo.

📸 **Captura:** esta celda.

### Valores de control de EXP-05 (si no salen, hay un error)

| Celda | Valor esperado |
|---|---|
| 3 | Aparecen `asistencias_15000.csv` y `tareas_15000.csv` |
| 5 | `Filas cargadas: 15000` |
| 6 | Vacíos 0 · A tiempo 13 869 · Tardanza 1 131 · `Salida antes de entrada: 0` · `Filas tras la limpieza: 15000` |
| 13 | Los tres formatos: `[('A tiempo', 13869), ('Tardanza', 1131)]` |
| 10, 11 y 12 | Bytes y segundos **no** tienen un valor fijo: anota los tuyos |
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

### Gráfico 1 · Asistencias por estado (sobre la Celda 7)
- X column: `Estado_Asistencia` · Y columns: `cantidad` · Data labels: activados

```
%md
**Qué demuestra:** cuántas de las 15 000 asistencias fueron a tiempo y cuántas con tardanza.
Lectura: predominan las asistencias a tiempo (13 869 frente a 1 131 tardanzas).
```

### Gráfico 2 · Tamaño en disco (sobre la Celda 12)
- X column: `formato` · Y columns: `bytes`
- Ejes: `Formato de almacenamiento` y `Tamaño en disco (bytes)` · Data labels con formato `0,0`
- Nombre de la pestaña: `Tamaño en disco: CSV vs Parquet vs Delta`

```
%md
**Qué demuestra:** cuánto espacio ocupan las mismas 15 000 asistencias según el formato en que se guardan.
CSV: ... bytes · Parquet: ... bytes · Delta: ... bytes.
Lectura: Parquet y Delta guardan los datos por columnas y comprimidos, por eso ocupan mucho menos que el CSV, que es texto plano. Delta suma su registro de cambios (_delta_log).
```

### Gráfico 3 · Velocidad de la consulta (sobre la Celda 12)
- X column: `formato` · Y columns: `consulta_mediana_s`, `consulta_minimo_s` y `consulta_maximo_s` (sin apilar: *Stacking* desactivado)
- Ejes: `Formato de almacenamiento` y `Tiempo de lectura + GROUP BY (s)` · Data labels `0.000`
- En la pestaña **Series** renombra las tres barras como `Mediana`, `Mínimo` y `Máximo`
- Nombre de la pestaña: `Latencia de la consulta por formato`

```
%md
**Qué demuestra:** cuánto tarda en leerse y agruparse por estado el mismo dato guardado en cada formato (1 calentamiento + 5 repeticiones).
Mediana: CSV ... s · Parquet ... s · Delta ... s.
Lectura: si los rangos mínimo–máximo se cruzan entre formatos, la diferencia no es concluyente con 15 000 filas.
```

### Gráfico 4 (opcional) · Velocidad de escritura (sobre la Celda 12)
- X column: `formato` · Y columns: `escritura_mediana_s` · Eje Y: `Tiempo de escritura (s)`


---

## 11. Paso 10 · Conclusión, capturas y entrega

### Celda final · Comparación y análisis (celda de texto)

Agrega una celda **+ Text** al final y completa los `...` con **tus** números. No inventes valores: copia los que salieron en tu notebook.

```
%md
## Comparación y análisis
- Formato más liviano: ...  (bytes)
- Formato con la consulta más rápida: ...  (mediana en segundos)
- Formato más rápido de escribir: ...
- Interpretación: Parquet y Delta guardan por columnas y comprimen; CSV es texto sin tipos. Delta agrega un registro de transacciones (_delta_log).
- Limitaciones: 15 000 filas, datos sintéticos, una sola sesión, compute serverless (no muestra uso de CPU ni RAM).
```

### Lista de capturas

El profesor pide documentar **objetivo, procedimiento y pasos, configuración, resultados, comparación y análisis** y **evidencias de ejecución**. En cada captura debe verse el **✓ verde con la hora**, y en ninguna debe aparecer tu correo.

- [ ] Catalog con esquema, volumen, carpetas `datos` y `salida` y los 2 CSV (Paso 5)
- [ ] Notebook con su nombre y **Serverless** conectado (Paso 6)
- [ ] Celda 1 · portada
- [ ] Celda 3 · comprobación de la ruta
- [ ] Celda 4 · contenido del archivo
- [ ] Celda 5 · DataFrame y conteo
- [ ] Celda 6 · EDA
- [ ] Celda 8 · tabla en el Catalog
- [ ] Celda 9 · consulta `GROUP BY`
- [ ] Celda 10 · tiempos de escritura
- [ ] Catalog con las carpetas `asist_csv`, `asist_parquet` y `asist_delta`
- [ ] Celda 11 · tamaño en disco
- [ ] Celda 12 · tabla de resultados
- [ ] Celda 13 · validación
- [ ] Gráficos 1, 2, 3 (y 4) con su texto de "Qué demuestra"
- [ ] Celda final · comparación y análisis

Guarda las capturas en la carpeta `capturas/` de esta misma carpeta del repositorio. El nombre final de cada captura lo define el grupo al integrar el informe.

### Exportar y entregar
1. **Exportar el notebook:** arriba, **File** (archivo) → **Export** (exportar) → **HTML**. Ese archivo es la evidencia completa de que todo se ejecutó.
2. **Descargar la tabla de resultados:** la de la **Celda 12**. Debajo de la tabla, pulsa el botón de descarga (flecha ⤓) y elige **CSV**. Guárdala en la carpeta `archivos-csv/`.
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

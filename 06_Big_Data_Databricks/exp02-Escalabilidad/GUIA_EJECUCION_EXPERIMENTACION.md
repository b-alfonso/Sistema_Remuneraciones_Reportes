# Guía de ejecución · EXP-02 Escalabilidad por volumen de datos

Proyecto: Base de Datos Avanzadas y Big Data · Grupo 2 · UPN
Carpeta del repositorio: `06_Big_Data_Databricks/exp02-Escalabilidad`
Datos: `asistencias_base.csv` / `tareas_base.csv` (582 filas), `*_5000.csv` y `*_10000.csv` (sintéticos)

Esta guía te lleva **desde que entras a Databricks hasta el último resultado**. No necesitas saber programar: el notebook ya tiene todo escrito; tú solo lo subes, lo ejecutas y revisas qué sale.

---

## 0. ¿Qué vamos a hacer?

Imagina una cocina: preparar 1 plato o 20 platos del mismo menú. Si la cocina es buena, preparar 20 no debería tardar 20 veces más.
Aquí la "cocina" es **Databricks** (con su motor **Apache Spark**) y los "platos" son filas de datos.

**La pregunta del experimento:** si cargo y consulto **582**, **5 000** y **10 000** filas de asistencias y tareas, ¿cuánto más tarda Databricks?

**El camino completo (mapa):**

```
 1. Entrar a Databricks
 2. Descargar el notebook de GitHub
 3. Subir (importar) el notebook a Databricks
 4. Conectar el compute Serverless
 5. Ejecutar todo con "Run all"
 6. Revisar cada resultado (capturas D-01 … T-03)
 7. Leer el gráfico final y sacar la conclusión
```

> 💡 **No tienes que subir los CSV a mano.** El notebook crea solo el esquema, el volumen y las carpetas, y copia los 6 CSV desde GitHub (`archivos-csv/`).

---

## 1. Antes de empezar: ¿qué necesitas?

| Necesitas | Para qué |
|---|---|
| Computadora con internet y Chrome o Edge | Databricks funciona en el navegador; no se instala nada |
| Un correo (Gmail sirve) | Para la cuenta gratuita de Databricks |
| El archivo `notebook/EXP02_Databricks_Rendimiento.ipynb` | Es el experimento completo |
| 15–20 minutos | La ejecución tarda entre 5 y 8 minutos |

---

## 2. Paso 1 · Entrar a Databricks

1. Entra a <https://www.databricks.com/learn/free-edition>.
2. Primera vez: **Sign up** (registrarse). Ya tienes cuenta: **Log in** (iniciar sesión).
3. Elige **Continue with Google** (continuar con Google) o escribe tu correo y copia el código que te llega.
4. Llegarás a **Home** (inicio). A la izquierda verás **Workspace**, **Catalog** y **New**.

> La *Free Edition* no pide tarjeta y ya trae el compute **Serverless** listo.
> 📸 No captures pantallas donde aparezca tu correo o tu código.

## 3. Paso 2 · Descargar el notebook

1. En GitHub abre `06_Big_Data_Databricks/exp02-Escalabilidad/notebook/EXP02_Databricks_Rendimiento.ipynb`.
2. Pulsa **Download raw file** (descargar archivo, icono de flecha hacia abajo, arriba a la derecha).
3. Se guarda un archivo `.ipynb` en tu carpeta de Descargas.

## 4. Paso 3 · Importar el notebook en Databricks

1. Menú izquierdo → **Workspace** (espacio de trabajo) → **Users** (usuarios) → tu correo.
2. Pulsa **⋮** (tres puntos, arriba a la derecha) → **Import** (importar).
3. Arrastra el `.ipynb` al recuadro y pulsa **Import**.
4. Haz clic en el nombre del notebook para abrirlo. Verás celdas de texto (explicaciones) y celdas de código.

## 5. Paso 4 · Conectar el compute

Arriba a la derecha hay un botón de cómputo. Debe decir **Serverless**.
Si dice **Connect** (conectar), púlsalo y elige **Serverless**.

## 6. Paso 5 · Ejecutar todo

1. Pulsa **Run all** (ejecutar todo).
2. Cada celda muestra un círculo girando mientras corre y una **✓ verde** cuando termina.
3. No cierres la pestaña hasta que termine la última celda (5–8 minutos).

> Si prefieres ir celda por celda: haz clic dentro de una celda y pulsa **Shift + Enter**. Así ves cada resultado con calma.

## 7. Paso 6 · Revisar los resultados

Cada salida imprime su código de captura. Comprueba que veas esto:

| Captura | Qué debes ver | Qué significa |
|---|---|---|
| **D-01** | Esquema `bd_rendimiento`, volumen `vol_rendimiento`, carpetas `datos_base` y `resultados` | El "estante" y la "caja" donde se guardan los datos |
| **D-02** | Los 6 CSV con su huella SHA-256 igual a la del manifiesto | Son exactamente los archivos del repositorio |
| **D-03 / D-04** | Primeras líneas de los CSV y los DataFrames con sus columnas | Spark leyó bien los archivos y los tipos |
| **D-05 / D-05b** | 188/15, 171/15 y 177/16 asistencias a tiempo/tardanza por mes | Mismos totales que el Data Mart (203, 186, 193) |
| **D-06** | Tablas `tb_asistencias` y `tb_tareas` | Los datos quedaron guardados como tablas Delta |
| **D-07** | TPA **92,10**, ICT **56,36**, TDT **3,44**, IEP **75,12** | Igual que Power BI: el cálculo es correcto |
| **D-08 / D-08b** | 5 000 y 10 000 filas por tabla | Las escalas grandes se cargaron completas |
| **D-09** | Spark, runtime y Python | Condiciones de la prueba |
| **T-01** | Tabla de 72 mediciones con estado `OK` y el resumen con mediana, mínimo y máximo | Los datos del experimento |
| **T-02** | Registro RUN-03 a RUN-05 y KPI por escala | Trazabilidad de cada corrida |
| **T-03** | Gráfico de tiempo frente a filas | El resultado del experimento (paso 7) |

> ⏱️ Los segundos exactos pueden variar un poco en tu cuenta (el compute es compartido). Lo importante es la **tendencia** y que los KPI den igual.

## 8. Paso 7 · Leer el gráfico y concluir

En **T-03**, el eje horizontal es el número de filas y el vertical los segundos. Cada punto es la mediana de 5 repeticiones.

- Si las líneas son **casi planas**, Databricks no tarda más con más datos: en este rango manda el costo fijo de arrancar cada operación.
- En la ejecución original: carga entre **1,78 y 2,29 s** y consulta entre **0,55 y 0,66 s** en las tres escalas.

**Conclusión esperada:** con hasta 10 000 filas por tabla los tiempos no aumentan con el volumen. No se puede afirmar lo mismo para millones de filas porque no se midieron.

---

## 9. Si algo falla

| Problema | Solución |
|---|---|
| *Attached cluster is terminated* | **Select resource** (elegir recurso) → **General compute** → **Serverless** → **Start, attach and run** |
| Una celda se queda en **Waiting** varios minutos | **Interrupt** (interrumpir) y vuelve a pulsar **Run all** |
| Error con `%fs` | Serverless no admite Scala; el notebook ya usa `dbutils.fs.head` |
| No copia los CSV desde GitHub | Súbelos a mano: **Catalog** → `workspace` → `bd_rendimiento` → `vol_rendimiento` → `datos_base` → **Upload to this volume** (subir a este volumen) y elige los 6 CSV de `archivos-csv/` |

## 10. Borrar todo al terminar (opcional)

```sql
%sql
DROP SCHEMA IF EXISTS workspace.bd_rendimiento CASCADE;
```

> Si después vas a ejecutar la solución Medallion (`../solucion_medallion`), no borres el esquema: Medallion lee los datos de ese volumen.

# Guía rápida: repetir los experimentos Big Data en Databricks (sin experiencia previa)

Esta guía es para alguien que **nunca ha usado Databricks**. En unos 20 minutos podrás repetir los dos notebooks de esta carpeta:

| Notebook | Qué hace | Tiempo de ejecución |
|---|---|---|
| **EXP-02** · `exp02-Escalabilidad/notebook/EXP02_Databricks_Rendimiento.ipynb` | Experimento: mide cuánto tarda cargar y consultar los datos con 582, 5 000 y 10 000 filas. | 5–8 min |
| **Medallion** · `solucion_medallion/BigData_Solucion_Medallion.ipynb` | Solución completa: limpieza, capas Bronze/Silver/Gold, indicadores y dashboard. | 3–5 min |

No necesitas instalar nada ni tener SQL Server: todo corre en el navegador y los datos ya están en GitHub.
Databricks está en inglés; abajo, cada botón lleva su traducción entre paréntesis.

---

## Paso 1 · Crear la cuenta gratuita (5 min)

1. Entra a <https://www.databricks.com/learn/free-edition> y pulsa **Sign up** (registrarse).
2. Elige **Continue with Google** (continuar con Google) o escribe tu correo.
3. Cuando termine, verás la página de inicio de Databricks (*Home*). Ya tienes un espacio de trabajo listo.

> La edición gratuita no pide tarjeta de crédito y ya incluye el cómputo (*Serverless*) que usan los notebooks.

## Paso 2 · Descargar los notebooks de GitHub (2 min)

1. En el repositorio, abre `06_Big_Data_Databricks/exp02-Escalabilidad/notebook/EXP02_Databricks_Rendimiento.ipynb`.
2. Pulsa el botón **Download raw file** (descargar archivo, icono de flecha hacia abajo, arriba a la derecha del archivo).
3. Repite con `06_Big_Data_Databricks/solucion_medallion/BigData_Solucion_Medallion.ipynb`.

Los CSV **no** hace falta descargarlos: EXP-02 los copia solo desde GitHub.

## Paso 3 · Subir los notebooks a Databricks (2 min)

1. En la barra izquierda pulsa **Workspace** (espacio de trabajo).
2. Entra a **Users** (usuarios) → tu correo.
3. Pulsa el menú **⋮** (tres puntos, arriba a la derecha) → **Import** (importar).
4. Arrastra el archivo `.ipynb` al recuadro y pulsa **Import**.
5. Repite con el segundo notebook.

## Paso 4 · Ejecutar un notebook (1 clic)

1. Abre el notebook haciendo clic en su nombre.
2. Arriba a la derecha, en el botón de cómputo, debe decir **Serverless**. Si dice **Connect** (conectar), púlsalo y elige **Serverless**.
3. Pulsa **Run all** (ejecutar todo).
4. Espera. Cada celda muestra un círculo girando mientras corre y una **✓ verde** cuando termina. No cierres la pestaña.

**Orden obligatorio:** primero EXP-02 y después Medallion. EXP-02 crea el esquema `bd_rendimiento`, el volumen `vol_rendimiento` y copia los CSV; Medallion lee los datos de ahí.

## Paso 5 · Comprobar que salió bien

### EXP-02 (experimento de escalado)

| Busca en el notebook… | Debe decir |
|---|---|
| Celda de verificación de archivos (captura D-02) | Los seis CSV listados, con su huella SHA-256 igual a la del manifiesto. |
| Celda de KPI de la línea base (D-07) | TPA **92,10**, ICT **56,36**, TDT **3,44**, IEP **75,12**. |
| Celda de mediciones (T-01) | Una tabla de 72 mediciones, todas con estado `OK`. |
| Gráfico final (T-03) | Dos líneas casi planas: los tiempos no suben de 582 a 10 000 filas. |

> Los segundos exactos pueden variar un poco en otra cuenta o en otro momento: es normal, porque el cómputo es compartido. Lo importante es la **tendencia** (que no crezcan con el volumen) y que los KPI den igual.

### Medallion (solución completa)

| Busca en el notebook… | Debe decir |
|---|---|
| S-02 | 582, 5 000 y 10 000 filas por tabla en Bronze. |
| S-07 | 0 filas descartadas y 527 tareas en cuarentena. |
| S-09 | `TODOS COINCIDEN` (KPI Gold = Power BI). |
| S-12 | Un enlace **Abrir el dashboard**: púlsalo para ver el tablero. |

Para ver el dashboard después: barra izquierda → **Dashboards** → "BASAV · Monitoreo de empleados (Gold)".

El significado de cada captura está en `exp02-Escalabilidad/capturas/README.md` y `solucion_medallion/capturas/README.md`.

## Si algo falla

| Mensaje o problema | Qué hacer |
|---|---|
| *Attached cluster is terminated* (el clúster está apagado) | Pulsa **Select resource** (elegir recurso) → **General compute** → **Serverless** → **Start, attach and run** (iniciar, conectar y ejecutar). |
| La celda se queda en **Waiting** (esperando) varios minutos | Pulsa **Interrupt** (interrumpir) y vuelve a pulsar **Run all**. |
| Error al usar `%fs` | No uses `%fs`: el cómputo Serverless no admite Scala. El notebook ya usa `dbutils.fs.head` en su lugar. |
| El dashboard no carga o no se crea | Barra izquierda → **SQL Warehouses** → enciende **Serverless Starter Warehouse** y vuelve a ejecutar solo la última celda. |
| *HAY DIFERENCIAS* en S-09 | Los CSV no son los del repositorio. Borra la carpeta `datos_base` del volumen y vuelve a ejecutar: el notebook los descargará de nuevo. |

## Borrar todo al terminar (opcional)

En una celda nueva escribe y ejecuta:

```sql
%sql
DROP SCHEMA IF EXISTS workspace.mon_bronze CASCADE;
DROP SCHEMA IF EXISTS workspace.mon_silver CASCADE;
DROP SCHEMA IF EXISTS workspace.mon_gold CASCADE;
DROP SCHEMA IF EXISTS workspace.bd_rendimiento CASCADE;
```

---
Más detalle técnico: [`exp02-Escalabilidad/README.md`](exp02-Escalabilidad/README.md) (EXP-02) y [`solucion_medallion/GUIA_REPLICACION.md`](solucion_medallion/GUIA_REPLICACION.md) (Medallion).

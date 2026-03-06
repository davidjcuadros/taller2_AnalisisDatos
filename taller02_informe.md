
# Taller 2 - Análisis de Datos

## 1. Configuración de la imagen de SQL Server

Descargamos la imagen de SQL Server y confirmamos que el proceso fue exitoso.

![alt text](images/image-0.png)
![alt text](images/image.png)

---

## 2. Ejecución del contenedor con los datos disponibles

Posteriormente ejecutamos el contenedor con SQL Server. Dentro de este contenedor restauramos la base de datos **AdventureWorks**.

Para este proceso utilizamos el comando **RESTORE DATABASE**, que permite reconstruir la base de datos a partir del archivo de respaldo (.bak).

Después de ejecutar el proceso verificamos que la base de datos **AdventureWorks** se encuentre correctamente disponible dentro del contenedor.

![alt text](images/image-2.png)
![alt text](images/image-11.png)

---

## 3. Generación del schema y los datos

Este proceso se realizó utilizando **SQL Server Management Studio (SSMS)**, que permite generar scripts SQL tanto para el **schema** como para los **datos** de una base de datos.

Para ello realizamos los siguientes pasos:

1. Nos conectamos a la base de datos AdventureWorks.
2. Utilizamos la opción **Generate Scripts** de SQL Server.
3. Generamos dos archivos `.sql`:

   * Uno con el **schema**
   * Otro con los **datos**

Estos archivos serían utilizados posteriormente para migrar la base de datos a PostgreSQL.

![alt text](images/image-3.png)

![alt text](images/image-4.png)
![alt text](images/image-5.png)

---

## 4. Generación de la base de datos en PostgreSQL

El taller solicitaba generar la base de datos en **PostgreSQL** a partir de los archivos:

* `schema_oltp.sql`
* `data_oltp.sql`

Sin embargo, inicialmente era necesario realizar varias modificaciones en estos archivos, ya que el **dialecto SQL de SQL Server es diferente al de PostgreSQL**.

Adicionalmente, el tamaño de los archivos era muy grande, lo cual impedía que el IDE utilizado (**Visual Studio Code**) pudiera abrirlos y modificarlos correctamente.

Debido a esto, se optó por utilizar un repositorio disponible en GitHub que contiene la base de datos **AdventureWorks adaptada para PostgreSQL**. En este repositorio los datos se cargan mediante múltiples archivos `.csv` que contienen la misma información.

Repositorio utilizado:

https://github.com/lorint/AdventureWorks-for-Postgres

![alt text](images/image-6.png)

Posteriormente verificamos que los datos se hubieran cargado correctamente ejecutando una consulta de prueba.

![alt text](images/image-7.png)

---

## 5. Creación del esquema OLAP

En esta fase se diseñó el **Data Warehouse** que permitirá responder las preguntas de negocio planteadas en el taller.

Para ello se creó el esquema **OLAP** y las tablas correspondientes:

* **fact_sales** (tabla de hechos)
* **dim_product** (dimensión de productos)
* **dim_customer** (dimensión de clientes)
* **dim_date** (dimensión de fechas)

Estas tablas siguen un modelo tipo **Star Schema**, que permite realizar análisis analíticos de forma eficiente.

![alt text](images/image-8.png)
![alt text](images/image-9.png)

---

## 6. Ejecución del proceso ETL

Posteriormente ejecutamos el script **main.py**, que implementa el proceso **ETL (Extract, Transform, Load)**.

Este proceso realiza:

**Extract**
Extracción de datos desde la base de datos PostgreSQL con el modelo transaccional (OLTP).

**Transform**
Transformación de los datos para adaptarlos al modelo analítico, incluyendo cálculos como:

* revenue
* margin
* cohortes de clientes

**Load**
Carga de los datos transformados en las tablas del esquema **OLAP**.

![alt text](images/image-10.png)

Finalmente verificamos que el proceso ETL se hubiera ejecutado correctamente realizando consultas sobre las tablas del Data Warehouse para confirmar que contienen datos.

![alt text](images/image-17.png)

---

## 7. Visualización en la aplicación web

Finalmente se ejecuta **app.py**, que corresponde a una aplicación web desarrollada en **Flask**.

Esta aplicación permite ejecutar las consultas analíticas creadas para responder las preguntas de negocio del taller.

Entre las consultas implementadas se encuentran:

* Porcentaje de ingresos provenientes de clientes recurrentes
* Productos con mayor varianza en el margen
* Análisis de Market Basket (productos comprados juntos)
* Análisis de cohortes de clientes

La aplicación web muestra los resultados de cada consulta en tablas dentro de la interfaz.

![alt text](images/image-12.png)
![alt text](images/image-13.png)
![alt text](images/image-14.png)

![alt text](images/image-15.png)

---



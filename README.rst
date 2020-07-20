============
project-name
============

Se necesita que el aspirante desarrolle una solución basada en Django Framework y
Django Rest Framework que cubra las necesidades requeridas en el sistema descrito a
continuación.
Tenemos la necesidad de poder subir archivos (.csv) al sistema de almacenamiento de
amazon web services (AWS S3) y crear una tabla en una base de datos externa
(diferente a la que usa el ORM de Django Framework) basada en el archivo, las
columnas de esta tabla deben corresponder al del archivo, y cuyos tipos de datos
pueden ser todos varchar o text, una vez subido, se debe leer el archivo
implementando ejecución por hilos para almacenar su información en la tabla creada.
Se debe garantizar que los datos guardados en las tablas creadas deben poder ser
consultados desde un endpoint, el cual, debe tener implementado paginación,
búsqueda por filtros y ordenamiento por columna.

Features:

- Read a bucket of S3 and load the last CSV file added.
- Save this file in a new table of a SQLlite DB
- Allows to query that table through a API REST services

Installation
============

#. Create new virtualenv with `python3 -m venv env`
#. Activate your virtualenv `source env/bin/activate`
#. Create .env file with and make sure it has all the env variables. This has to be in smk_project.


Configuration
=============

You need the following env variables in your file .env. This has to be in the folder smk_project.
You have to fill the variables related to AWS with your access data.
DOTENV=true
DJANGO_DEBUG=true

AWS_ACCESS_ID=""
AWS_ACCESS_KEY=""
AWS_BUCKET_NAME=""

IMPORT_DB_NAME="sqlite:///imported_csv_data.db"

Usage
=====
You can start to use this tool following these steps:
#. Upload a CSV file in your bucket
#. Run the command `python manage.py load_data`
#. You can also run the tests with `python manage.py test` 
#. Besides, you can execute a request using the API REST Example: GET http://127.0.0.1:8000/importer/query_table/?some_param_to_filer=anyvalue&

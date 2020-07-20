============
Symetrik Importer of CSV files
============

Applicant is required to develop a solution based on Django Framework and
Django Rest Framework that covers the needs required in the system described in
continuation.
We need to be able to upload files (.csv) to the storage system of
amazon web services (AWS S3) and create a table in an external database
(different from the one used by the Django Framework ORM) based on the file, the
columns of this table must correspond to that of the file, and whose data types
can be all varchar or text, once uploaded, the file must be read
implementing thread execution to store your information in the created table.
It must be guaranteed that the data saved in the created tables must be able to be
consulted from an endpoint, which must have pagination implemented,
search by filters and sort by column.

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
#. Upload a CSV file in your bucket
#. Run the command `python manage.py load_data`
#. You can also run the tests with `python manage.py test` 
#. Besides, you can execute a request using the API REST Example: GET http://127.0.0.1:8000/importer/query_table/?some_param_to_filer=anyvalue&order_by=any_param

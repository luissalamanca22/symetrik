# Stdlib imports
import io
import os

# Core Django imports
from django.conf import settings

# Third-party app imports
import boto3
from sqlalchemy import (
    Column, Integer, Float, Date,
    String, VARCHAR, MetaData, Table,
    select
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query
import marshmallow
import pandas as pd

# Imports from your apps
from .helpers import format_filename_as_tablename

Base = declarative_base()


class CSVImporter:
    """Class to import a csv to a new table in the given database"""

    def __init__(self, tablename: str = None):
        """
        :param filename: CSV file to be imported.
        :param tablename: Name of the table where the data will be dumped.
        """
        self._tablename = tablename
        self._create_database()
        self.bucket = None
        self.filename = None

    @property
    def tablename(self):
        return self._tablename or format_filename_as_tablename(self.filename)

    @tablename.setter
    def tablename(self, value):
        self._tablename = value

    @property
    def bucket(self):
        if not self._bucket:
            self._set_bucket()
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        self._bucket = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if value and os.path.splitext(value)[1].lower() != ".csv":
            raise ValueError("The file has to be a CSV")
        self._filename = value

    def _set_bucket(self):
        """
        Uses the current AWS crendentials and connects to S3,
        then set the bucket by default.
        """
        s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_ID,
            aws_secret_access_key=settings.AWS_ACCESS_KEY
        )
        self._bucket = s3.Bucket(settings.AWS_BUCKET_NAME)

    def _create_database(self):
        """Creates a new local sqlite DB"""
        self._engine = create_engine(settings.IMPORT_DB_NAME)
        Base.metadata.create_all(self._engine)

    def _read_csv_file(self) -> pd.DataFrame:
        """Read the current file and returns a dataframe"""
        return pd.read_csv(self.filename)

    @staticmethod
    def sort_files_by_modfied_date(files):
        return sorted(
            files,
            key=lambda obj: int(obj.last_modified.strftime('%s')),
            reverse=True
        )

    def retrieve_and_save_last_csv_file_from_s3(self):
        """Retrieve all the files in the default bucket and 
        filters the last one added
        """
        files = self.bucket.objects.all()
        files = filter(lambda obj: obj.key.endswith(".csv"), files)
        files_sorted = self.sort_files_by_modfied_date(files)
        try:
            # The most recent file should be first
            last_file_added = files_sorted[0]
        except IndexError:
            raise Exception("There are no files in the bucket")
        else:
            self.bucket.download_file(last_file_added.key, last_file_added.key)
            self.filename = last_file_added.key

    def import_cvs_file_to_table(self):
        """Import the current CSV file into a new table"""
        assert self.filename, "A filename has to be provided"
        assert self.tablename, "A tablename has to be provided"
        df = self._read_csv_file()
        df.to_sql(con=self._engine, index_label='id',
                  name=self.tablename, if_exists='replace')
        os.remove(self.filename)


class DBModel:
    """ 
    This class allows to interact with the database and serialize data
    of a Query. 
    """
    engine = None
    MAX_NUM_RECORDS = 10

    @staticmethod
    def get_results(
        tablename: str,
        filters: dict = {},
        order_by: str = None,
        page: int = 1
    ):
        """"
        With the given table creates a query applying 
        to it the filters, order and limit
        """
        DBModel.engine = create_engine(settings.IMPORT_DB_NAME)

        metadata = MetaData()
        table = Table(tablename, metadata, autoload=True,
                      autoload_with=DBModel.engine)

        Session = sessionmaker(bind=DBModel.engine)
        session = Session()
        query = session.query(table)

        if filters and isinstance(filters, dict):
            query = query.filter_by(**filters)
        if order_by:
            query = query.order_by(order_by)
        query = query.limit(DBModel.MAX_NUM_RECORDS).offset(page or 1)
        return query

    @staticmethod
    def serialize_results(query: Query):
        """
        Converts the results of the given query in a 
        serialized data.
        :param query: 
        """
        types = {
            "default": marshmallow.fields.String()
        }
        TableSchema = type('TableSchema', (marshmallow.Schema,), {
            attr["name"]: types["default"]
            for attr in query.column_descriptions
        })
        schema = TableSchema()
        return schema.dump(query, many=True)

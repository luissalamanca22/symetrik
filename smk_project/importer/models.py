import io
import os

from django.conf import settings

import pandas as pd
import boto3

from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    @property
    def tablename(self):
        return self._tablename or format_filename_as_tablename(self.filename)

    @tablename.setter
    def tablename(self, value):
        self._tablename = value

    def _create_database(self):
        """Creates a new local sqlite DB"""
        self.engine = create_engine(settings.IMPORT_DB_NAME)
        Base.metadata.create_all(self.engine)

    def _read_csv_file(self) -> pd.DataFrame:
        """Read the current file and returns a dataframe"""
        return pd.read_csv(self.filename)

    def retrieve_and_save_last_csv_file_from_s3(self):
        """Retrieve all the files in the default bucket and 
        filters the last one added
        """
        s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_ID,
            aws_secret_access_key=settings.AWS_ACCESS_KEY
        )
        bucket = s3.Bucket(settings.AWS_BUCKET_NAME)

        files = bucket.objects.all()
        files_sorted = sorted(
            files,
            key=lambda obj: int(obj.last_modified.strftime('%s')),
            reverse=True
        )
        last_file_added = files_sorted[0]
        bucket.download_file(last_file_added.key, last_file_added.key)
        self.filename = last_file_added.key

    def import_cvs_file_to_table(self):
        """Import the current CSV file into a new table"""
        assert self.filename, "A filename has to be provided"
        assert self.tablename, "A tablename has to be provided"
        df = self._read_csv_file()
        df.to_sql(con=self.engine, index_label='id',
                  name=self.tablename, if_exists='replace')
        os.remove(self.filename)

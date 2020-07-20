from django.test import TestCase

from django.conf import settings

from rest_framework.test import APITestCase

from importer.models import (
    DBModel,
    CSVImporter
)

class CSVImporterTestCase(TestCase):
    """---"""

    def setUp(self):
        self.importer = CSVImporter()

    def test_settings(self):
        self.assertIsNotNone(settings.AWS_BUCKET_NAME)
        self.assertIsNotNone(settings.AWS_ACCESS_ID)
        self.assertIsNotNone(settings.AWS_ACCESS_KEY)
        self.assertIsNotNone(settings.IMPORT_DB_NAME)

    def test_connect_to_amazon_and_set_bucket(self):
        self.assertEquals(self.importer.bucket.name, settings.AWS_BUCKET_NAME)

    def test_creation_of_database(self):
        self.importer._create_database()
        self.assertIsNotNone(self.importer._engine)

    def test_sort_of_files(self):
        files = self.importer.bucket.objects.all()
        sorted_files = self.importer.sort_files_by_modfied_date(files)
        if len(sorted_files) > 1:
            self.assertGreater(
                sorted_files[0].last_modified.strftime('%s'), 
                sorted_files[1].last_modified.strftime('%s')
            )

    def test_retrieve_and_save_last_csv_file_from_s3(self):
        self.importer.retrieve_and_save_last_csv_file_from_s3()
        self.assertIsNotNone(self.importer.filename)

    def test_import_cvs_file_to_table_raise_error(self):
        self.assertRaises(AssertionError, self.importer.import_cvs_file_to_table)

    def test_success_importation_of_file(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker, Query
        from sqlalchemy import MetaData, Table

        self.importer.retrieve_and_save_last_csv_file_from_s3()
        self.importer.import_cvs_file_to_table()

        engine = create_engine(settings.IMPORT_DB_NAME)
        metadata = MetaData()
        table = Table(self.importer.tablename, metadata, autoload=True, autoload_with=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(table)
        self.assertGreater(query.count(), 0)


class DBModelTestCase(TestCase):

    def setUp(self):
        self.importer = CSVImporter()
        self.importer.retrieve_and_save_last_csv_file_from_s3()
        self.importer.import_cvs_file_to_table()

    def test_get_results(self):
        query = DBModel.get_results(self.importer.tablename)
        self.assertGreater(query.count(), 0)

    def test_serialize_results(self):
        query = DBModel.get_results(self.importer.tablename)
        data = DBModel.serialize_results(query)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from importer.models import CSVImporter


class ImportedTablesApiViewAPITestCase(APITestCase):

    def setUp(self):
        pass

    def test_query_table_request_fails(self):
        """Checks that the service return an error when the table doesn't exist"""
        url = reverse("importer:query_table", kwargs={"tablename": "fake_table"} )
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _test_query_table_request_success(self):
        """Verifica que el servicio responda"""
        importer = CSVImporter()
        importer.retrieve_and_save_last_csv_file_from_s3()
        importer.import_cvs_file_to_table()

        url = reverse("importer:query_table", kwargs={"tablename": importer.tablename} )
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)


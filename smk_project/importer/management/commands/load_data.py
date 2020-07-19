from django.core.management.base import BaseCommand, CommandError
from importer.models import CSVImporter

class Command(BaseCommand):
    help = 'Load the data from CSV files saved in a S3 Bucket and load it in a DB.'

    def handle(self, *args, **options):
        importer = CSVImporter()
        importer.retrieve_and_save_last_csv_file_from_s3()
        importer.import_cvs_file_to_table()
        self.stdout.write(self.style.SUCCESS("Successfully data loaded"))
from django.core.management.base import BaseCommand

from geographical_module.models import Geography
from geographical_module.utils import get_csv_reader_from_remote, bulk_create_update_from_csv

REMOTE_FILE_PATH = 'https://package-files.s3.eu-central-1.amazonaws.com/+django-geographical-module/geographies.csv'


class Command(BaseCommand):
    help = 'Load geographical data (e.g. NUTS) into the database'

    def handle(self, **options):
        print("Started...")
        print("Loading csv from remote...")
        reader = get_csv_reader_from_remote(REMOTE_FILE_PATH)
        print("Preparing data to be created or updated...")
        bulk_create_update_from_csv(model=Geography, csv_reader=reader)

        print("Finished.")

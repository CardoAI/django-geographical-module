from django.core.management.base import BaseCommand

from geographical_module.scripts.nuts_postcode import create_nuts_postcode_records_for_db


class Command(BaseCommand):
    help = 'Load nuts3-postcode data from csv file into the database'

    def handle(self, **options):
        create_nuts_postcode_records_for_db()

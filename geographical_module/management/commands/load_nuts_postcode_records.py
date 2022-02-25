import time

from django.core.management.base import BaseCommand

from geographical_module.models import GeographyPostcode, Geography
from geographical_module.utils import get_csv_reader_from_remote

REMOTE_FILE_PATH = "https://package-files.s3.eu-central-1.amazonaws.com/+django-geographical-module/nuts_postcodes.csv"


class Command(BaseCommand):
    help = 'Load nuts-postcode data from remote CSV file into the database.'

    def handle(self, **options):
        print("Loading NUTS-Postcode data from remote CSV file...")
        nuts_postcodes_reader = get_csv_reader_from_remote(REMOTE_FILE_PATH, delimiter=';')

        print("Loading existing NUTS-Postcode into memory...")
        existing_nuts_postcodes_records = GeographyPostcode.objects.exclude(
            geography__nuts_code=None
        )
        existing_combinations = set(existing_nuts_postcodes_records.values_list(
            "geography__nuts_code",
            "postcode"
        ))

        print("Loading NUTS records ids into memory...")
        nuts_ids = {
            record.nuts_code: record.id
            for record in Geography.objects.exclude(nuts_code=None)
        }

        print("Processing NUTS-Postcode data...")

        time0 = time.time()

        records_to_create = []
        index = 0
        for row in nuts_postcodes_reader:

            if (row["nuts"], row["postcode"]) not in existing_combinations:
                try:
                    geography_id = nuts_ids[row["nuts"]]
                except KeyError:
                    # Geography with the given code does not exist, skip
                    continue

                records_to_create.append(GeographyPostcode(
                    geography_id=geography_id,
                    postcode=row["postcode"]
                ))

            if index % 100000 == 0:
                print(f"{index} records processed...")
            index += 1

        time1 = time.time()
        print("Finished processing rows in ", time1 - time0, "seconds.")

        print("Creating NUTS-Postcode records...")
        time0 = time.time()

        GeographyPostcode.objects.bulk_create(records_to_create, batch_size=200000)

        time1 = time.time()
        print("Finished creating records in ", time1 - time0, " seconds.")

        print("Done.")

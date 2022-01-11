from django.core.management.base import BaseCommand
from django.core.management import call_command

fixtures = [
    "nuts.yaml",
]


class Command(BaseCommand):
    help = 'Load geographical data (e.g. NUTS) from fixture into the database'

    def handle(self, **options):
        for fixture in fixtures:
            print(f"Loading fixture {fixture}")
            call_command("loaddata", fixture)

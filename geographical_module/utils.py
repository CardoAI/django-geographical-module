import csv
import io
from urllib.request import urlopen

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import QuerySet


def get_or_none(queryset: QuerySet, *args, **kwargs):
    try:
        return queryset.get(*args, **kwargs)
    except ObjectDoesNotExist:
        return None


def get_csv_reader_from_remote(remote_path: str, delimiter=","):
    """
    Read a csv file from a remote server and return a DictReader object
    """
    with urlopen(remote_path) as file:
        mycsv = io.StringIO(file.read().decode())
        return csv.DictReader(mycsv, delimiter=delimiter)


FIELDS_FROM_EMPTY_STRING_TO_NONE = ['iso_3166_code','nuts_code','alpha_2', 'alpha_3']


def bulk_create_update_from_csv(model: models.Model.__class__, csv_reader: csv.DictReader, batch_size=500):
    """
    1. Read model records from a given csv_reader and
    2. Form two lists with objects to create and update
    3. Use bulk_create and bulk_update to commit to the database
    """
    records_to_create = []
    records_to_update = []
    _ids = set(model.objects.values_list('id', flat=True))
    for row in csv_reader:
        for field in FIELDS_FROM_EMPTY_STRING_TO_NONE:
            if row[field] == '':
                row[field] = None
        if int(row['id']) in _ids:
            records_to_update.append(model(**row))
        else:
            records_to_create.append(model(**row))

    csv_reader.fieldnames.remove('id')

    model.objects.bulk_create(
        records_to_create,
        batch_size=batch_size
    )
    model.objects.bulk_update(
        records_to_update,
        fields=csv_reader.fieldnames,
        batch_size=batch_size
    )

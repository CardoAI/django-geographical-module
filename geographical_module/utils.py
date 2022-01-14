from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from model_utils import Choices

STANDARDS = Choices(
    (0, "unspecified", "Unspecified"),
    (1, "nuts", "NUTS"),
    (2, "iso_3166", "ISO 3166"),
)


def get_or_none(queryset: QuerySet, *args, **kwargs):
    try:
        return queryset.get(*args, **kwargs)
    except ObjectDoesNotExist:
        return None

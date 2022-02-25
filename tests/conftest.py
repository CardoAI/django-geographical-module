import pytest as pytest

from geographical_module.models import Geography


@pytest.fixture
def initial_geographies():
    top_parent = Geography.objects.create(level=0, original_name='TopParent1', nuts_code='T1')
    Geography.objects.create(level=0, original_name='TopParent2', nuts_code='T2')

    Geography.objects.create(
        level=1,
        original_name='Level 1',
        nuts_code='C1',
        parent=top_parent,
        top_parent=top_parent
    )

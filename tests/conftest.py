import pytest as pytest

from geographical_module.models import Geography


@pytest.fixture
def create_data():
    top_parent = Geography.objects.create(level=0, original_name='TopParent', code='T0')
    data_dict = {
        'top_parent': top_parent,
        'lvl_1_p': Geography.objects.create(level=1, original_name='TopParent', parent=top_parent,
                                            code='C1',
                                            top_parent=top_parent),
        'dummy_parent': Geography.objects.create(level=0, original_name='Dummy', code='D0'),

    }
    return data_dict

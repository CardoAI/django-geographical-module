import pytest
from django.core.exceptions import ValidationError

from geographical_module.models import Geography, GeographyPostcode


@pytest.mark.django_db
def test_geography_model_creation_hierarchy(create_data):
    cases_to_test_data = [
        # Top_parent : top_parent has parents
        {'level': 0, 'code': 'T1', 'original_name': 'Child',
         'parent': create_data['lvl_1_p']},
        {'level': 0, 'code': 'T1', 'original_name': 'Child',
         'top_parent': create_data['lvl_1_p']},
        # Wrong parents: parent and top_parent are different
        {'level': 1, 'code': 'T2', 'original_name': 'Child',
         'parent': create_data['top_parent']},
        {'level': 1, 'code': 'T2', 'original_name': 'Child',
         'top_parent': create_data['top_parent']},
        {'level': 3, 'code': 'T2', 'original_name': 'Child',
         'parent': create_data['lvl_1_p'],
         'top_parent': create_data['dummy_parent']},
        # Wrong level: self.level is not == parent_level + 1
        {'level': 3, 'code': 'T3', 'original_name': 'Child',
         'parent': create_data['lvl_1_p'],
         'top_parent': create_data['top_parent']}
    ]

    for case in cases_to_test_data:
        with pytest.raises(ValidationError):
            Geography.objects.create(**case)


@pytest.mark.django_db
def test_get_geography_by_postcode(create_data):
    g_p = GeographyPostcode.objects.create(geography=create_data['lvl_1_p'], postcode='A123')

    # Correct geography-postcode is returned by  'Geography.get_child_by_post_code' method
    assert create_data['top_parent'].get_child_by_post_code(g_p.postcode) == g_p

    # Geography instance must be of level 0' rule enforced
    with pytest.raises(AssertionError):
        _ = create_data['lvl_1_p'].get_child_by_post_code('empty')

    # No geography-postcode was found
    assert create_data['top_parent'].get_child_by_post_code('empty') is None

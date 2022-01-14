import pytest

from geographical_module.models import Geography


@pytest.mark.django_db
@pytest.mark.parametrize(
    'record_data',
    [
        # Case 1: Level 0 with parent
        {'level': 0, 'parent': "TopParent1"},
        # Case 2: Level 0 with top parent
        {'level': 0, 'top_parent': "TopParent1"},
        # Case 3: Non-zero level without top-parent
        {'level': 1, 'parent': "TopParent1"},
        # Case 4: Non-zero level without parent
        {'level': 1, 'top_parent': "Level 1"},
        # Case 5: Level 1 with parent different from top-parent
        {'level': 1, 'parent': "TopParent1", 'top_parent': "TopParent2"},
        # Case 6: self.level is not == parent_level + 1
        {'level': 3, 'parent': "TopParent1", 'top_parent': "TopParent2"}
    ]
)
def test_create_geography_raises_error(record_data, initial_geographies):
    with pytest.raises(AssertionError):
        parent = top_parent = None
        if parent_name := record_data.pop('parent', None):
            parent = Geography.objects.get(original_name=parent_name)
        if top_parent_name := record_data.pop('top_parent', None):
            top_parent = Geography.objects.get(original_name=top_parent_name)

        Geography.objects.create(
            **record_data,
            parent=parent,
            top_parent=top_parent,
            code="T1",
        )


@pytest.mark.django_db
def test_get_geography_by_postcode_returns_correct_record(initial_geographies):
    level_1 = Geography.objects.get(original_name="Level 1")
    g_p = level_1.postcodes.create(postcode="A123")

    assert level_1.parent.get_child_by_post_code(g_p.postcode) == g_p, \
        "Incorrect geography is returned!"

    assert level_1.parent.get_child_by_post_code('empty') is None, \
        "Incorrect geography is returned!"


@pytest.mark.django_db
def test_get_geography_by_postcode_when_level_gt_0_raises_error(initial_geographies):
    level_1 = Geography.objects.get(original_name="Level 1")

    with pytest.raises(AssertionError):
        level_1.get_child_by_post_code('empty')

import pytest
from django.core.exceptions import ValidationError

from geographical_module.models import Geography, GeographyPostcode


@pytest.mark.django_db
class TestModels:

    def test_geography_model_creation_hierarchy(self):
        top_parent = Geography.objects.create(level=0, original_name='TopParent', code='T0')
        lvl_1_p = Geography.objects.create(level=1, original_name='TopParent', parent=top_parent,
                                           code='C1',
                                           top_parent=top_parent)
        dummy_parent = Geography.objects.create(level=0, original_name='Dummy', code='D0')

        with pytest.raises(ValidationError):
            """Geography lvl=0 has a parent: level 0 geography can not be connected to parents"""
            Geography.objects.create(level=0, code='T2', original_name='Child', parent=lvl_1_p,
                                     top_parent=top_parent)

        with pytest.raises(ValidationError):
            """Wrong parents: parent and top_parent are different"""
            Geography.objects.create(level=1, code='T1', original_name='Child', parent=top_parent)
            Geography.objects.create(level=3, code='T2', original_name='Child', parent=lvl_1_p,
                                     top_parent=dummy_parent)

        with pytest.raises(ValidationError):
            """Wrong level: self.level is not == parent_level + 1 """
            Geography.objects.create(level=3, code='T2', original_name='Child', parent=lvl_1_p,
                                     top_parent=top_parent)

    def test_get_geography_by_postcode(self):
        top_parent = Geography.objects.create(level=0, original_name='TopParent', code='T0')
        lvl_1_p = Geography.objects.create(level=1, original_name='TopParent', parent=top_parent,
                                           code='C1',
                                           top_parent=top_parent)

        g_p = GeographyPostcode.objects.create(geography=lvl_1_p, postcode='A123')

        """ Correct geography-postcode is returned by  'Geography.get_child_by_post_code' method"""
        assert top_parent.get_child_by_post_code(g_p.postcode) == g_p

        """ 'Geography instance must be of level 0' rule inforced """
        with pytest.raises(AssertionError):
            _ = lvl_1_p.get_child_by_post_code('empty')

        """No geography-postcode was found"""
        assert top_parent.get_child_by_post_code('empty') == None

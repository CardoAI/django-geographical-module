from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models

from geographical_module.utils import STANDARDS, get_or_none


class Geography(models.Model):
    level = models.PositiveSmallIntegerField()
    original_name = models.CharField(max_length=256, help_text="Original name in the native language.")
    en_name = models.CharField(max_length=256, null=True, help_text="English name.")
    code = models.CharField(max_length=16, unique=True, help_text="Code as defined by a standard.")
    standard = models.IntegerField(choices=STANDARDS, default=STANDARDS.unspecified,
                                   help_text="The standard this code is defined by.")
    parent = models.ForeignKey(to='self', related_name='children', null=True, on_delete=models.CASCADE)
    top_parent = models.ForeignKey(to='self', related_name='bottom_children', null=True, on_delete=models.CASCADE)

    def clean(self):
        """Make sure that new records that are added respect the hierarchy."""
        if self.level != 0 and not (self.parent_id and self.top_parent_id):
            raise ValidationError("Top parent and parent can not be None if level of Geography is 0!")
        if self.parent and self.parent.top_parent_id is not None and self.parent.top_parent_id != self.top_parent_id:
            raise ValidationError("Top parent can not be different from parent's top parent!")

        return super(Geography, self).clean()

    def save(self, *args, **kwargs,):
        self.clean()
        return super(Geography, self).save(*args, **kwargs)

    def get_child_by_post_code(self, postcode: str) -> Optional["Geography"]:
        """
        Find the child geography of a level zero geography by postcode.

        Args:
            postcode: The postcode to search for.
        """

        assert self.level == 0, "Geography instance must be of level 0."

        return get_or_none(
            GeographyPostcode.objects,
            postcode=postcode,
            geography__top_parent=self
        )

    def __str__(self):
        return f'{self.en_name or self.original_name}-{self.code}'


class GeographyPostcode(models.Model):
    """Links a postcode to a geography."""

    geography = models.ForeignKey(to='Geography', on_delete=models.CASCADE, related_name="postcodes")
    postcode = models.CharField(max_length=16)

    class Meta:
        unique_together = ('geography', 'postcode')

    def __str__(self):
        return f'{self.geography.code}-{self.postcode}'

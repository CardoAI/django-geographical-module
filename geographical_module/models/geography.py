from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models

from geographical_module.utils import STANDARDS, get_or_none


class Geography(models.Model):
    level = models.PositiveSmallIntegerField()
    original_name = models.CharField(max_length=256, null=True, help_text="Original name in the native language.")
    en_name = models.CharField(max_length=256, null=True, help_text="English name.")
    code = models.CharField(max_length=16, help_text="Code as defined by a standard.")
    standard = models.IntegerField(choices=STANDARDS, default=STANDARDS.unspecified,
                                   help_text="The standard this code is defined by.")
    parent = models.ForeignKey(to='self', related_name='children', null=True, on_delete=models.CASCADE)
    top_parent = models.ForeignKey(to='self', related_name='bottom_children', null=True, on_delete=models.CASCADE)
    alpha_2 = models.CharField(max_length=16, null=True, unique=True)
    alpha_3 = models.CharField(max_length=16, null=True, unique=True)

    class Meta:
        unique_together = [('standard', 'code')]

    # Todo-still work to be done
    def _verify(self):
        """Make sure that new records that are added respect the hierarchy."""
        if self.level == 0 and (self.parent_id or self.top_parent_id):
            raise ValidationError("Geography of level 0 can not have parent and top_parent!")
        elif self.level != 0:
            if self.parent and self.top_parent:
                if self.parent and self.parent.top_parent_id is None and self.parent != self.top_parent:
                    raise ValidationError("Top parent can not be different from parent's top parent!")
                elif self.parent and self.parent.top_parent_id is not None and self.parent.top_parent_id != self.top_parent_id:
                    raise ValidationError("Top parent can not be different from parent's top parent!")
            elif not (self.parent and self.top_parent):
                raise ValidationError("Parent and top_parent must be provided since level is not 0!")
            if self.parent and self.level != self.parent.level + 1:
                raise ValidationError("The Geography level is not one level below the parent level!")

    def save(self, *args, **kwargs, ):
        self._verify()
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

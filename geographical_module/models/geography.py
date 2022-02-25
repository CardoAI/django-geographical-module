from typing import Optional

from django.db import models

from geographical_module.utils import get_or_none


class ContinentChoices(models.TextChoices):
    ASIA = 'asia', 'Asia'
    AFRICA = 'africa', 'Africa'
    EUROPE = 'europe', 'Europe'
    NORTH_AMERICA = 'north_america', 'North America'
    SOUTH_AMERICA = 'south_america', 'South America'
    AUSTRALIA = 'australia', 'Australia'
    ANTARCTICA = 'antarctica', 'Antarctica'


class Geography(models.Model):
    continent = models.CharField(max_length=16, choices=ContinentChoices.choices)
    level = models.PositiveSmallIntegerField()
    original_name = models.CharField(max_length=256, null=True,
                                     help_text="Original name in the native language.")
    en_name = models.CharField(max_length=256, null=True, help_text="English name.")

    nuts_code = models.CharField(max_length=16, unique=True, null=True, help_text="Code as defined by NUTS standard.")
    iso_3166_code = models.CharField(max_length=16, unique=True, null=True, help_text="Code as defined by ISO 3166 standard.")

    parent = models.ForeignKey(to='self', related_name='children', null=True,
                               on_delete=models.CASCADE)
    top_parent = models.ForeignKey(to='self', related_name='bottom_children', null=True,
                                   on_delete=models.CASCADE)
    alpha_2 = models.CharField(max_length=16, null=True, unique=True)
    alpha_3 = models.CharField(max_length=16, null=True, unique=True)

    def _verify(self):
        """Make sure that new records that are added respect the hierarchy."""
        if self.level == 0:
            assert self.parent_id is None, "Level 0 can not have parent!"
            assert self.top_parent_id is None, "Level 0 can not have top parent!"
        else:
            assert self.parent is not None and self.top_parent is not None, \
                "Level > 0 must have parent and top parent!"

            assert self.level == self.parent.level + 1, \
                "The level must be one below the parent's!"

            if self.level == 1:
                assert self.parent == self.top_parent, \
                    "Level 1 must have the same parent and top parent!"
            else:
                assert self.parent.top_parent_id == self.top_parent_id, \
                    "Top parent can not be different from parent's top parent!"

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
        return f'{self.en_name or self.original_name}'


class GeographyPostcode(models.Model):
    """Links a postcode to a geography."""

    geography = models.ForeignKey(to='Geography', on_delete=models.CASCADE,
                                  related_name="postcodes")
    postcode = models.CharField(max_length=16)

    class Meta:
        unique_together = ('geography', 'postcode')

    def __str__(self):
        return f'{self.geography.nuts_code}-{self.postcode}'

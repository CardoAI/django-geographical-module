from django.db import models
from django.core.exceptions import ValidationError


class Geography(models.Model):
    level = models.PositiveSmallIntegerField()
    original_name = models.CharField(max_length=256)
    en_name = models.CharField(max_length=256, null=True)
    code = models.CharField(max_length=16, unique=True)
    parent = models.ForeignKey(to='self', related_name='children', null=True,
                               on_delete=models.CASCADE)
    top_parent = models.ForeignKey(to='self', related_name='bottom_children', null=True,
                                   on_delete=models.CASCADE)

    def clean(self):
        if self.top_parent != self.parent.top_parent != None:
            raise ValidationError("Top parent can not be different from parent's top parent!")
        return super(Geography, self).clean()

    def __str__(self):
        return f'{self.original_name}-{self.code}'


class NutsPostcode(models.Model):
    class Meta:
        unique_together = ('nuts', 'postcode')

    nuts = models.CharField(max_length=16)
    postcode = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.nuts}-{self.postcode}'

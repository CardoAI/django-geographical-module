from django.db import models


class Geography(models.Model):
    level = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=16, unique=True)
    parent = models.ForeignKey(to='self', related_name='children', null=True,
                               on_delete=models.CASCADE)
    top_parent = models.ForeignKey(to='self', related_name='bottom_children', null=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}-{self.code}'

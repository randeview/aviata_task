from django.db import models


class City(models.Model):
    name = models.CharField('Названия', max_length=255)
    code = models.CharField('Код', max_length=4)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

import datetime

from django.db import models


class Directory(models.Model):
    long_name = models.CharField(max_length=225)
    short_name = models.CharField(max_length=20)
    description = models.TextField(max_length=255)
    version = models.CharField(max_length=20, null=False, unique=True)
    date_time = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return self.short_name


class DirectoryElement(models.Model):
    directories = models.ForeignKey(Directory, on_delete=models.CASCADE)
    element_code = models.CharField(max_length=20, null=True)
    element_value = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"

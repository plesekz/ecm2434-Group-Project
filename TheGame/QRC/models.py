from django.db import models
from Resource.models import Resource
from django.core.validators import MinLengthValidator


class QRC(models.Model):
    QRID = models.PositiveIntegerField()
    latitude = models.DecimalField()
    longitude = models.DecimalField()

    def __str__(self):
        return self.QRID


class QRResource(models.Model):
    QRID = models.ForeignKey(QRC, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return self.QRID
     

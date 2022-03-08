from django.db import models
from Resources.models import Resource
from django.core.validators import MinLengthValidator


class QRC(models.Model):
    QRID = models.PositiveIntegerField(unique=True)
    latitude = models.DecimalField(decimal_places=4, max_digits=6)
    longitude = models.DecimalField(decimal_places=4, max_digits=6)

    def __str__(self):
        return str(self.QRID)


class QRResource(models.Model):
    QRID = models.ForeignKey(QRC, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.QRID) + str(self.resource)
     
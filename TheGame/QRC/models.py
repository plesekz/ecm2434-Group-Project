from django.db import models
from django.core.validators import MinLengthValidator


class Resource(models.Model):
    codeID = models.IntegerField(max_length=5)
    resourceType = models.IntegerField(max_length=3, validators=[MinLengthValidator(3)])
    amount = models.IntegerField(max_length=2)
    latitude = models.DecimalField(max_length=32)
    longitude = models.DecimalField(max_length=32)

    def __str__(self):
        return self.resourceID

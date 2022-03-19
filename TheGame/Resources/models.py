from django.db import models
from Login.models import Player

# Create your models here.

# model for representing a resource in the database


class Resource(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# model for representing a link between player their resources in the database


class PlayerResource(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.player) + " has " + \
            str(self.amount) + " " + str(self.resource)

from django.db import models
from Login.models import Player 

# Create your models here.

class Resource(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PlayerResource(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.player) + " has " + str(self.amount) + " " + str(self.resource)

# class QRResources(model.Model):
#     qr = models.ForeignKey(QRCode, on_delete=models.CASCADE)
#     resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

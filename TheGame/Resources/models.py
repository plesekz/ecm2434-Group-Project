from django.db import models
from Login.models import Player 

# Create your models here.

class Resource(models.Model):
    name = models.CharField(max_length=50)

class PlayerResource(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

# class QRResources(model.Model):
#     qr = models.ForeignKey(QRCode, on_delete=models.CASCADE)
#     resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

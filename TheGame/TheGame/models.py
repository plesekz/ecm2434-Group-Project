from django.db import models
from Login.models import Player

class pStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    pHealth = models.PositiveIntegerField(default=0)
    pToughness = models.PositiveIntegerField(default=0)
    pEvasion = models.PositiveIntegerField(default=0)
    damage = models.PositiveIntegerField(default=0)
    accuracy = models.PositiveIntegerField(default=0)
    attackSpeed = models.PositiveIntegerField(default=0)
    aHealth = models.PositiveIntegerField(default=0)
    aToughness = models.PositiveIntegerField(default=0)
    aEvasion = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.player.username)
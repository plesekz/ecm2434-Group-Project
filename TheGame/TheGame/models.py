from turtle import speed
from django.db import models

class pStat(models.Model):
    username = models.CharField(max_length=50)
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
        return str(self.username)
from concurrent.futures.process import _threads_wakeups
from unicodedata import decimal
from django.db import models
from Login.models import Player

class Champion(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    #sprites = somedata()
    #items = somedata()

    pHealth = models.PositiveIntegerField(default=100)
    pToughness = models.PositiveIntegerField(default=1)
    pEvasion = models.PositiveIntegerField(default=0)
    damage = models.PositiveIntegerField(default=1)
    accuracy = models.PositiveIntegerField(default=1)
    attackSpeed = models.PositiveIntegerField(default=1)
    aHealth = models.PositiveIntegerField(default=0)
    aToughness = models.PositiveIntegerField(default=0)
    aEvasion = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    type = models.CharField(max_length=15)

    damageReduction = models.IntegerField()
    damgeScaling = models.DecimalField(decimal_places=2)
    specialEffect = models.CharField(max_length=20)

class ChampionItems(models.Model):
    champion = models.ForeignKey(Champion)
    item = models.ForeignKey(Item)
    amount = models.IntegerField()
    itemLevel = models.IntegerField()
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
    type = models.CharField(max_length=32)

    Stat1 = models.IntegerField(default=1)
    Stat2 = models.IntegerField(default=1)
    Stat3 = models.IntegerField(default=1)
    def __str__(self):
        return str(self.name)

class ChampionItems(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    itemLevel = models.IntegerField()


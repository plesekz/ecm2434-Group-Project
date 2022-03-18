from argparse import ArgumentDefaultsHelpFormatter
from concurrent.futures.process import _threads_wakeups
from unicodedata import decimal
from django.db import models
from Login.models import Player
from polymorphic.models import PolymorphicModel

class Champion(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    #sprites = somedata()
    #items = somedata()

    pHealth = models.PositiveIntegerField(default=100)
    pAthletics = models.PositiveIntegerField(default=1)
    pBrain = models.PositiveIntegerField(default=1)
    pControl = models.PositiveIntegerField(default=1)
    
    primaryWeapon
    secondaryWeapon

    armour
    auxItem1
    auxItem2
    auxItem3

    def __str__(self):
        return str(self.name)

class Item(PolymorphicModel):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def __str__(self):
        return "item: " + self.name

class BaseItem(Item):
    armourValue = models.IntegerField()
    vitalityBoost = models.IntegerField()

    specialAbilities = models.CharField(max_length=50)

    def __str__(self):
        return "BaseItem: " + self.name

class SpecificItem(BaseItem):
    # contains defaults for items
    level = models.IntegerField()
    glory = models.IntegerField()

    def __str__(self):
        return "SpecificItem: " + self.name + ", lvl: " + str(self.level)

class BaseWeapon(Item):
    damageNumber = models.IntegerField()
    damageInstances = models.IntegerField()
    range = models.IntegerField()
    associated = models.CharField(max_length=1)

    def __str__(self):
        return "BaseWeapon: " + self.name

class SpecificWeapon(BaseWeapon):
    level = models.IntegerField()
    glory = models.IntegerField()

    def __str__(self):
        return "SpecificWeapon: " + self.name + ", lvl: " + str(self.level)

class ChampionItems(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.champion) + " " +  str(self.item)
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

    armourValue = models.IntegerField(default=1)
    vitalityBoost = models.IntegerField(default=1)
    
    specialAbilities = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

class Weapon(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    type = models.CharField(max_length=32)

    damageNumber = models.IntegerField()
    damageInstances = models.IntegerField()
    range = models.IntegerField()

class ChampionItems(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    itemLevel = models.IntegerField()
    glory = models.IntegerField()


from polymorphic.models import PolymorphicModel

class tItem(PolymorphicModel):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def __str__(self):
        return "item: " + self.name

class BaseItem(tItem):
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
        return "Specificitem: " + self.name

class BaseWeapon(tItem):
    damageNumber = models.IntegerField()
    damageInstances = models.IntegerField()
    range = models.IntegerField()

    def __str__(self):
        return "BaseWeapon: " + self.name

class SpecificWeapon(BaseWeapon):
    level = models.IntegerField()
    glory = models.IntegerField()

    def __str__(self):
        return "SpecificWeapon: " + self.name

class tChampionItems(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(tItem, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.champion) + " " +  str(self.item)
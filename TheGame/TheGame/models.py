from argparse import ArgumentDefaultsHelpFormatter
from concurrent.futures.process import _threads_wakeups
from unicodedata import decimal
from django.db import models
from Login.models import Player
from polymorphic.models import PolymorphicModel
from Resources.models import Resource


class Item(PolymorphicModel):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    priceRes1 = models.ForeignKey(Resource, null=False,
         related_name="priceRes1", on_delete=models.CASCADE)
    price1 = models.IntegerField(null=False)

    priceRes2 = models.ForeignKey(Resource, null=True,
         related_name="priceRes2", on_delete=models.CASCADE)
    price2 = models.IntegerField(null=True)

    priceRes3 = models.ForeignKey(Resource, null=True,
         related_name="priceRes3", on_delete=models.CASCADE)
    price3 = models.IntegerField(null=True)    

    def __str__(self):
        return "item: " + self.name

class BaseItem(Item):
    armourValue = models.IntegerField()
    vitalityBoost = models.IntegerField()
    shieldValue = models.IntegerField()

    specialAbilities = models.CharField(max_length=50)

    def __str__(self):
        return f"Armour Value: {self.armourValue}<br>Vitality Boost: {self.vitalityBoost}<br>Ability: {self.specialAbilities}"


class SpecificItem(BaseItem):
    # contains defaults for items
    level = models.IntegerField()
    glory = models.IntegerField()

    def __str__(self):
        return f"Armour Value: {self.armourValue}<br>Vitality Boost: {self.vitalityBoost}<br>Ability: {self.specialAbilities}<br>Level: {self.level}<br>Glory: {self.glory}"


class BaseWeapon(Item):
    damageNumber = models.IntegerField()
    damageInstances = models.IntegerField()
    range = models.IntegerField()
    associated = models.CharField(max_length=1)
    ap_cost = models.IntegerField()

    def __str__(self):
        return f"Damage: {self.damageNumber}<br>Speed: {self.damageNumber}<br>Range: {self.damageNumber}<br>AP Cost: {self.ap_cost}"


class SpecificWeapon(BaseWeapon):
    level = models.IntegerField()
    glory = models.IntegerField()

    def __str__(self):
        return f"Damage: {self.damageNumber}<br>Range: {self.damageNumber}<br>AP Cost: {self.ap_cost}<br>Level: {self.level}<br>Glory: {self.glory}"


class Champion(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    #sprites = somedata()
    #items = somedata()

    pHealth = models.PositiveIntegerField(default=100)
    pAthletics = models.PositiveIntegerField(default=1)
    pBrain = models.PositiveIntegerField(default=1)
    pControl = models.PositiveIntegerField(default=1)

    primaryWeapon = models.ForeignKey(
        SpecificWeapon,
        on_delete=models.CASCADE,
        related_name="pWeapon",
        null=True)
    secondaryWeapon = models.ForeignKey(
        SpecificWeapon,
        on_delete=models.CASCADE,
        related_name="sWeapon",
        null=True)

    armour = models.ForeignKey(
        SpecificItem,
        on_delete=models.CASCADE,
        related_name="armour",
        null=True)
    auxItem1 = models.ForeignKey(
        SpecificItem,
        on_delete=models.CASCADE,
        related_name="aux1",
        null=True)
    auxItem2 = models.ForeignKey(
        SpecificItem,
        on_delete=models.CASCADE,
        related_name="aux2",
        null=True)
    auxItem3 = models.ForeignKey(
        SpecificItem,
        on_delete=models.CASCADE,
        related_name="aux3",
        null=True)

    def __str__(self):
        return str(self.name)


class ChampionItems(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
<<<<<<< HEAD
        return str(self.name)

class Item (models.Model):
    ## item stats
    type = models.CharField(max_length="20")
    damageReduction = models.PositiveIntegerField()
    damageScaling = models.DecimalField()
=======
        return str(self.champion) + " " + str(self.item)
>>>>>>> 0b419260c2c3597aabbd465953f4868ea279668b

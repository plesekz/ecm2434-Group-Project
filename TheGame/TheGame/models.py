from argparse import ArgumentDefaultsHelpFormatter
from concurrent.futures.process import _threads_wakeups
from unicodedata import decimal
from django.db import models
from Login.models import Player
from polymorphic.models import PolymorphicModel

class Item(PolymorphicModel):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return "item: " + self.name

class BaseItem(Item):
    armourValue = models.IntegerField()
    vitalityBoost = models.IntegerField()

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
        return f"Damage: {self.damageNumber}<br>Speed: {self.damageNumber}<br>Range: {self.damageNumber}<br>AP Cost: {self.ap_cost}<br>Level: {self.level}<br>Glory: {self.glory}"

class Champion(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    #sprites = somedata()
    #items = somedata()

    pHealth = models.PositiveIntegerField(default=100)
    pAthletics = models.PositiveIntegerField(default=1)
    pBrain = models.PositiveIntegerField(default=1)
    pControl = models.PositiveIntegerField(default=1)
    
    primaryWeapon = models.ForeignKey(SpecificWeapon, on_delete=models.CASCADE, related_name="pWeapon", null=True)
    secondaryWeapon = models.ForeignKey(SpecificWeapon, on_delete=models.CASCADE, related_name="sWeapon", null=True)

    armour = models.ForeignKey(SpecificItem, on_delete=models.CASCADE, related_name="armour", null=True)
    auxItem1 = models.ForeignKey(SpecificItem, on_delete=models.CASCADE, related_name="aux1", null=True)
    auxItem2 = models.ForeignKey(SpecificItem, on_delete=models.CASCADE, related_name="aux2", null=True)
    auxItem3 = models.ForeignKey(SpecificItem, on_delete=models.CASCADE, related_name="aux3", null=True)

    def __str__(self):
        return str(self.name)

class ChampionItems(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.champion) + " " +  str(self.item)
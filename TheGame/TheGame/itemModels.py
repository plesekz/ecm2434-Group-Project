from django.db import models
from polymorphic.models import PolymorphicModel
from TheGame.models import *

class tItem(PolymorphicModel):
    name = models.CharField(max_length=50)
    price = models.CharField()
    type = models.CharField()

    def __str__(self):
        return "item: " + self.name

class BaseItem(tItem):
    armourValue = models.IntegerField()
    vitalityBoost = models.IntegerField()

    specialAbilities = models.CharField()

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
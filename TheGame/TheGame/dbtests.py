from TheGame.models import *
from TheGame.processes import getChampion

def runtest():
    ringItem = Item.objects.create(name="ring",
        price=5, 
        type="accessory"
    )
    print(str(ringItem))

    ringBase = BaseItem.objects.create(
        name = ringItem.name,
        price = ringItem.price,
        type = ringItem.type,

        armourValue = 10,
        vitalityBoost = 100,
        specialAbilities = "swiftness"
    )
    print(str(ringBase))

    ringSpecific = SpecificItem.objects.create(
        name = ringBase.name,
        price = ringBase.price,
        type = ringBase.type,

        armourValue = ringBase.armourValue + 14,
        vitalityBoost = ringBase.vitalityBoost + 45,
        specialAbilities = ringBase.specialAbilities,

        level=5,
        glory=500,
    )

    print(str(ringSpecific))


    champ = getChampion(Player.objects.get(username="alex"))
    print(str(champ))

    ChampionItems.objects.create(
        champion = champ,
        item = ringSpecific,
        amount=1,
    )
    
    ci = ChampionItems.objects.get(
        champion=champ,
        item__type = "accessory"
    )
    print(str(ci))

def runbigtest():
    ringItem = Item.objects.create(name="ring",
        price=5, 
        type="accessory"
    )
    print(str(ringItem))

    ringBase = BaseItem.objects.create(
        name = ringItem.name,
        price = ringItem.price,
        type = ringItem.type,

        armourValue = 10,
        vitalityBoost = 100,
        specialAbilities = "swiftness"
    )
    print(str(ringBase))

    ringSpecific = SpecificItem.objects.create(
        name = ringBase.name,
        price = ringBase.price,
        type = ringBase.type,

        armourValue = ringBase.armourValue + 14,
        vitalityBoost = ringBase.vitalityBoost + 45,
        specialAbilities = ringBase.specialAbilities,

        level=5,
        glory=500,
    )

    print(str(ringSpecific))

    swordItem = Item.objects.create(name="shortSword",
        price=50,
        type="weapon"
    )

    swordBase = BaseWeapon.objects.create(
        name = swordItem.name,
        price = swordItem.price,

        damageNumber = 25,
        damageInstances = 2,
        range = 12
    )

    swordSpecific = SpecificWeapon.objects.create(
        name = swordBase.name,
        price = swordBase.price,

        damageNumber = swordBase.damageNumber + 14,
        damageInstances = swordBase.damageInstances + 2,
        range = swordBase.range,

        level = 5,
        glory = 2
    )

    champ = getChampion(Player.objects.get(username="alex"))
    print(str(champ))

    ChampionItems.objects.create(
        champion = champ,
        item = ringSpecific,
        amount=1,
    )

    ChampionItems.objects.create(
        champion = champ,
        item = swordSpecific,
        amount=1,
    )
    
    cis = ChampionItems.objects.filter(
        champion=champ,
    )

    for ci in cis:
        print(str(ci))
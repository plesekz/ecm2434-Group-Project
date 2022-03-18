from TheGame.models import *
from TheGame.processes import getChampion

def runtest():
    ringItem = tItem.objects.create(name="ring",
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

    tChampionItems.objects.create(
        champion = champ,
        item = ringSpecific,
        amount=1,
    )
    
    ci = tChampionItems.objects.get(
        champion=champ,
        item__type = "accessory"
    )
    print(str(ci))

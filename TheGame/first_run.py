from TheGame.models import Champion
from TheGame.processes import createNewBaseItem, createNewBaseWeapon
from Resources.models import Resource

circuitry = Resource.objects.create(
    name="Circuitry"
)

books = Resource.objects.create(
    name="Books"
)

machine_parts = Resource.objects.create(
    name="Machine parts"
)

createNewBaseItem("Salvaged armour", "armour", 10, 0, 0, "", circuitry, 10)
createNewBaseItem("Aux1", "aux", 1, 0, 0, "", circuitry, 1)
createNewBaseItem("Aux2", "auax", 3, 2, 0, "", circuitry, 2)
createNewBaseWeapon("Shiv", "weapon", 15, 1, 1, "A", 2, books, 2)
createNewBaseWeapon("Makeshift rifle", "weapon", 12, 2, 10, "C", 2, machine_parts, 2, books, 1)
createNewBaseWeapon("Self-taught psionics", "weapon", 5, 5, 5, "B", 2, machine_parts, 5)
createNewBaseItem("Large Armour Upgrade Pack", "statPack", 50, 5, 0, "", machine_parts, 15)
Champion.objects.create(
            player=None,
            name="Average Joe",
            pHealth=1,
            pAthletics=1,
            pBrain=1,
            pControl=1,

            primaryWeapon = None,
            armour = None,
            auxItem1 = None,
            auxItem2 = None,
            auxItem3 = None,
            sprite = "hacker"
        )

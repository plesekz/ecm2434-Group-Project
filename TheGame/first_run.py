from platform import machine
from TheGame.models import Champion
from TheGame.processes import createNewBaseItem, createNewBaseWeapon, createNewSpecificItem
from Resources.models import Resource

#
# CREATE SOME RESOURCES IN THE SYSTEM
#

circuitry = Resource.objects.create(
    name="Circuitry"
)

books = Resource.objects.create(
    name="Books"
)

machine_parts = Resource.objects.create(
    name="Machine parts"
)

bottle_caps = Resource.objects.create(
    name = "Bottle caps"
)

anti_matter = Resource.objects.create(
    name = "Anti matter"
)

neon_light_fluid = Resource.objects.create(
    name = "Neon light fluid"
)

metal_scraps = Resource.objects.create(
    name = "Metal Scraps"
)

plutonium_sticks = Resource.objects.create(
    name = "Plutonium sticks"
)


#
# CREATE SOME BASE ITEMS FOR THE GAME
#

salvaged_armour = createNewBaseItem("Salvaged armour", "armour", 10, 0, 0, "", circuitry, 10)
createNewBaseItem("Sheet metal armour", "armour", 20, 0, 10, "", metal_scraps, 50, bottle_caps, 20)
createNewBaseItem("Laser armour", "armour", 70, 10, 55, "", neon_light_fluid, 35, circuitry, 25, plutonium_sticks, 30)
createNewBaseItem("Atomic armour", "armour", 100, 0, 40, "", plutonium_sticks, 45, neon_light_fluid, 35, anti_matter, 50)

createNewBaseItem("Ring", "aux", 1, 0, 0, "", metal_scraps, 5)
createNewBaseItem("Necklace", "auax", 3, 2, 0, "", bottle_caps, 2, books, 5)
createNewBaseItem("Visor", "aux", 5, 5, 15, "", neon_light_fluid, 10, circuitry, 5)
createNewBaseItem("Smart watch", "aux", 0, 0, 10, "", circuitry, 10, metal_scraps, 10)
createNewBaseItem("Anti matter pocket watch", "aux", 100, 100, 100, "", anti_matter, 1000000)

#
# CREATE SOME WEAPONS FOR THE GAME
#

createNewBaseWeapon("Shiv", "weapon", 15, 1, 1, "A", 2, books, 2)
createNewBaseWeapon("Makeshift rifle", "weapon", 12, 2, 10, "C", 2, machine_parts, 2, books, 1)
createNewBaseWeapon("Self-taught psionics", "weapon", 5, 5, 5, "B", 2, machine_parts, 5)
laser_sword = createNewBaseWeapon("Laser Sword", "weapon", 30, 4, 5, "C", 5, plutonium_sticks, 30, metal_scraps, 15)
laser_gun = createNewBaseWeapon("Laser gun", "weapon", 10, 8, 100, "A", 3, plutonium_sticks, 45, metal_scraps, 20)
createNewBaseWeapon("Neon bombs", "weapon", 100, 1, 15, "B", 8, plutonium_sticks, 32, anti_matter, 15)
createNewBaseWeapon("Dance battle bomb", "weapon", 0, 0, 15, "dance dance baby!", 10, metal_scraps, 100, plutonium_sticks, 30, anti_matter, 15)
createNewBaseWeapon("Bigly sized anti matter bomb", "weapon", 1000000, 1, 20, "C", 15, anti_matter, 1000000)

#
# CREATE SOME UPGRADE PACKS FOR THE GAME
#

createNewBaseItem("Large Armour Upgrade Pack", "statPack", 50, 5, 0, "", machine_parts, 15)
createNewBaseItem("Small armour Upgrade Pack", "statPack", 10, 0, 0, "", bottle_caps, 5)
createNewBaseWeapon("Weapon sharpener", "statPack", 20, 0, 0, "", 0, metal_scraps, 15, machine_parts, 15)
createNewBaseWeapon("Weapon lightener", "statPack", 0, 2, 0, "", 0, books, 15, plutonium_sticks, 15)



Champion.objects.create(
            player=None,
            name="Catt Mollison",
            pHealth=150,
            pAthletics=15,
            pBrain=15,
            pControl=15,

            primaryWeapon = createNewSpecificItem(laser_gun, 15, 15),
            armour = createNewSpecificItem(salvaged_armour, 15, 15),
            auxItem1 = None,
            auxItem2 = None,
            auxItem3 = None,
            sprite = "hacker"
        )

Champion.objects.create(
            player=None,
            name="Rick Noss",
            pHealth=150,
            pAthletics=15,
            pBrain=15,
            pControl=15,

            primaryWeapon = createNewSpecificItem(laser_sword, 15, 15),
            armour = createNewSpecificItem(salvaged_armour, 15, 15),
            auxItem1 = None,
            auxItem2 = None,
            auxItem3 = None,
            sprite = "hacker"
        )

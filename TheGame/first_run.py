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

createNewBaseItem("Salvaged armour", "armour", 10, 0, "", circuitry, 10)
createNewBaseWeapon("Shiv", "weapon", 15, 1, 1, "A", 2, books, 2)
createNewBaseWeapon("Makeshift rifle", "weapon", 12, 2, 10, "C", 2, machine_parts, 2, books, 1)
createNewBaseWeapon("Self-taught psionics", "weapon", 5, 5, 5, "B", 2, machine_parts, 5)

from TheGame.processes import createNewBaseItem, createNewBaseWeapon
from Resources.models import Resource

createNewBaseItem("Salvaged armour", 0, "armour", 10, 0, "")
createNewBaseWeapon("Shiv", 0, "weapon", 15, 1, 1, "A", 2)
createNewBaseWeapon("Makeshift rifle", 0, "weapon", 12, 2, 10, "C", 2)
createNewBaseWeapon("Self-taught psionics", 10, "weapon", 5, 5, 5, "B", 2)

Resource.objects.create(
    name="Circuitry"
)

Resource.objects.create(
    name="Books"
)

Resource.objects.create(
    name="Machine parts"
)

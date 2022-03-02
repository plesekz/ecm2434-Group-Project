## adding resources
to add a resource to a user there should be a function that takes a user model and a resource model and an amount,

it will then query the database to check if this user has any of this resource already:\  if not then the resource/player relation will be added to the database with the amount specified \  if yes then the amount of that resource that the player has will be incremented by the specified amount

this function will be availiable at `Resources.processes.addResourceFromUser`
function will have signiture `def addResourceToUser(user : Player, resource : Resource, amount : int) -> None:`

## removing resources
to remove resources from a user you there will be a function that takes a user model and resource model and an amount

the function will check that the relation between the player/resource exists: \  if yes then it will check the player has enough to remove the specified amount and if they do then that amount will be removed otherwise and error will be raised \  if no then an error will be raised

this function will be availiable at `Resources.processes.removeResourceFromUser`
function will have signiture `def removeResourceFromUser(user : Player, resource : Resource, amount : int) -> None:`
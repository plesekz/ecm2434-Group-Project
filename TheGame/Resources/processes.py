from tokenize import String
from django.http import HttpResponse, HttpResponseRedirect
from Resources.models import PlayerResource, Resource
from Login.models import Player

def addResourceToUser(user : Player, resource : Resource, amount : int) -> None:
    '''function to add an amount of a resource to a user

    Args:
        user (Player): model object for the player you want to add to
        resource (Resource): model object for the resource you want to add
        amount (int): the amount of the given resource you want to add

    be sure to wrap this function in a try/catch block as it will throw Exceptions
    that should be dealt with
    '''

    if not (pr := user.playerresource_set.filter(resource=resource)):
        user.playerresource_set.create(resource=resource, amount=amount)
    else:
        pr[0].amount += amount
        pr[0].save()

def removeResourceFromUser(user : Player, resource : Resource, amount : int) -> None:
    '''function to remove an amount of a resource to a user

    Args:
        user (Player): model object for the player you want to remove from
        resource (Resource): model object for the resource you want to remove
        amount (int): the amount of the given resource you want to remove

    be sure to wrap this function in a try/catch block as it will throw Exceptions
    that should be dealt with
    it will throw and exception is the user does not have enough resources
    '''

    if not (pr := user.playerresource_set.filter(resource=resource)).exists():
        raise Exception("this player has never had this resource")

    playerRes = pr[0]

    if playerRes.amount < amount:
        raise Exception("this player does not have enough resource")

    playerRes.amount = playerRes.amount - amount
    playerRes.save()

def getAllUserResources(user : Player) -> "list[tuple[Resource, int]]":
    """function to return a list of all resources and amounts associated with a user

    Args:
        user (Player): the user that you would like to get resources of

    Returns:
        (list[tuple[Resource, int]]) list of tuples for each resource the user has in format (Resource, amount)
    """

    resList = user.playerresource_set.all()
    returnList = []

    for res in resList: 
        returnList.append((res.resource, res.amount))

    return returnList


def getResourceByName(name : String) -> Resource:
    """returns a resource given its name

    Args:
        name(String): the name of the resource

    Returns:
        (Resource): the resource object correlating to the name
    """
    if (not (res := Resource.objects.filter(name=name)).exists()):
        return None

    return res[0]

def getAllResources() -> "list[Resource]":
    """function that returns all avaliable resources in the database

    Returns:
        (list[Resource]) list of all the resources in the database
    """
    resources = Resource.objects.all()

    return resources

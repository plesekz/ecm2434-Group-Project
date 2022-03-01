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

    ##code
    ## if player already has this resource then increment
    if (pr := PlayerResource.objects.filter(resource=resource, player=user)).exists():
        relation = pr[0]
        relation.amount += amount
        relation.save()
    else:   ## create this player-resource relation
        relation = PlayerResource.objects.create(
            player=user, resource=resource, amount=amount
        )
        relation.save()

def removeResourceFromUser(user : Player, resource : Resource, amount : int) -> None:
    '''function to remove an amount of a resource to a user

    Args:
        user (Player): model object for the player you want to remove from
        resource (Resource): model object for the resource you want to remove
        amount (int): the amount of the given resource you want to remove

    be sure to wrap this function in a try/catch block as it will throw Exceptions
    that should be dealt with
    '''
    ##code
    # check the player has this resource
    if not (pr := PlayerResource.objects.filter(resource=resource, player=user)).exists():
        raise Exception('player does not have these resources')
    relation = pr[0]
    
    # make sure that the player has enough resources to remove
    if relation.amount < amount:
        raise Exception('player does not have sufficient resources')

    # remove the resources
    relation.amount -= amount
    relation.save()

def getAllUserResources(user : Player):
    """function to return a list of all resources and amounts associated with a user

    Args:
        user (Player): the user that you would like to get resources of
    """

    #check if the user has any resources
    if not (playerResources := PlayerResource.objects.filter(player=user)).exists():
        return []

    ##iterate throught resources and add them to list
    resourceList = []
    for pr in playerResources:
        resourceList.append((pr.resource, pr.amount))

    return resourceList

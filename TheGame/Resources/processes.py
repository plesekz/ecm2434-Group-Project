from django.http import HttpResponse, HttpResponseRedirect
from Resources.models import PlayerResource, Resource
from Login.models import Player

def addResourceToUser(user : Player, resource : Resource, amount : int) -> None:
    ##code
    ## if player already has this resource then increment
    if (pr := PlayerResource.objects.filter(resource=resource, user=user)).exists():
        relation = pr[0]
        relation.amount += amount
        relation.save()
    else:   ## create this player-resource relation
        relation = PlayerResource.objects.create()
        relation.user = user
        relation.resource = resource
        relation.amount = amount
        relation.save()

def removeResourceFromUser(user : Player, resource : Resource, amount : int) -> None:
    ##code
    if not (pr := PlayerResource.objects.filter(resource=resource, user=user, amount=amount)).exists():
        raise Exception('player does not have these resources')
    relation = pr[0]
    
    if relation.amount < amount:
        raise Exception('player does not have sufficient resources')

    relation.amount -= amount
    relation.save()

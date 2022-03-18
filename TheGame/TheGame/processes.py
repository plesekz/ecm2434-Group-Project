from logging import exception
from operator import truediv
from django.http import HttpRequest, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from Login.models import Player
from Resources.processes import removeResourceFromUser, addResourceToUser, getResourceByName
from .models import Champion
from Login.processes import getUserFromCookie
from Login.models import Player
from Resources.models import PlayerResource, Resource

def getUserFromName(request):
    """ returns a users stat block,
    you should probably use getChampion instead
    """
    user = getUserFromCookie(request)
    userStats = Champion.objects.get(player=user)
    return userStats

def getChampion(player : Player) -> Champion:
    if not (champs := Champion.objects.filter(player=player)).exists():
        return None

    return champs[0]


def spendResource(request, rNeeded, amount):
    """ spends a requested amount of a resource from a user
    """
    try:
        removeResourceFromUser(getUserFromCookie(request), getResourceByName(rNeeded), amount)
        return True
    except Exception as e:
        messages.error(request, ('Not enough resources'))
        return False

def buyPHealth(request):
    """ makes a purchase of pHealth from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.pHealth += 1
        userStats.save()
    
    return response

def buyPToughness(request):
    """ makes a purchase of pToughness from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")

    addResourceToUser(getUserFromCookie(request), getResourceByName('wood'), 5)
    userStats = getUserFromName(request)
    userStats.pToughness += 1
    userStats.save()    

    return response

def buyPEvasion(request):
    """ makes a purchase of pEvasion from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.pEvasion += 1
        userStats.save()    

    return response

def buyDamage(request):
    """ makes a purchase of damage from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.damage += 1
        userStats.save()
    
    return response

def buyAccuracy(request):
    """ makes a purchase of accuracy from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.accuracy += 1
        userStats.save()    

    return response

def buyAttackSpeed(request):
    """ makes a purchase of attackSpeed from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.attackSpeed += 1
        userStats.save()    

    return response

def buyAHealth(request):
    """ makes a purchase of aHealth from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.aHealth += 1
        userStats.save()
    
    return response

def buyAToughness(request):
    """ makes a purchase of aToughness from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.aToughness += 1
        userStats.save()    

    return response

def buyAEvasion(request):
    """ makes a purchase of aEvasion from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.aEvasion += 1
        userStats.save()

    return response


def getAllBosses() -> "list[Champion]":

    if not (bosses := Champion.objects.filter(player=None)):
        return None

    bossList = []

    for b in bosses:
        bossList.append(b)

    return bossList

def addBossToSystem(request : HttpRequest):
    if not request.method == "POST":
        return HttpResponse("failed to perform operation")

    statInfo = request.POST;

    Champion.objects.create(
        player=None,
        name = statInfo['name'],
        pHealth =  statInfo['pHealth'],
        pToughness = statInfo['pToughness'],
        pEvasion = statInfo['pEvasion'],
        damage = statInfo['damage'],
        accuracy = statInfo['accuracy'],
        attackSpeed = statInfo['attackSpeed'],
        aHealth = statInfo['aHealth'],
        aToughness = statInfo['aToughness'],
        aEvasion = statInfo['aEvasion'],
    )

    return HttpResponseRedirect('addBosses')
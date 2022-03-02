from logging import exception
from operator import truediv
from django.shortcuts import redirect
from django.contrib import messages
from Login.models import Player
from Resources.processes import removeResourceFromUser, addResourceToUser, getResourceByName
from .models import pStat
from Login.processes import getUserFromCookie
from Login.models import Player
from Resources.models import PlayerResource, Resource

def getUserFromName(request):
    user = getUserFromCookie(request)
    userStats = pStat.objects.get(player=user)
    return userStats

def spendResource(request, rNeeded, amount):
    try:
        removeResourceFromUser(getUserFromCookie(request), getResourceByName(rNeeded), amount)
        return True
    except Exception as e:
        messages.error(request, ('Not enough resources'))
        return False

def buyPHealth(request):
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
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if addResourceToUser(getUserFromCookie(request), getResourceByName('wood'), 5):
        userStats = getUserFromName(request)
        userStats.pToughness += 1
        userStats.save()    

    return response

def buyPEvasion(request):
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
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.aEvasion += 1
        userStats.save()

    return response
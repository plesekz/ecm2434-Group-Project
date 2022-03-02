from django.shortcuts import redirect
from django.contrib import messages
from Login.models import Player
from Resources.processes import removeResourceFromUser, addResourceToUser
from .models import pStat
from Login.processes import getUserFromCookie
from Login.models import Player
from Resources.models import PlayerResource, Resource

def getUserFromName(request):
    user = getUserFromCookie(request)
    userStats = pStat.objects.get(player=user)
    return userStats

def buyPHealth(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    removeResourceFromUser(getUserFromCookie(), 'wood', 1)
    userStats = getUserFromName(request)
    userStats.pHealth += 1
    userStats.save()
    response = redirect("characterMenu")

    return response

def buyPToughness(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    addResourceToUser(getUserFromCookie(), 'wood', 5)
    userStats = getUserFromName(request)
    userStats.pToughness += 1
    userStats.save()
    response = redirect("characterMenu")

    return response

def buyPEvasion(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    userStats = getUserFromName(request)
    userStats.pEvasion += 1
    userStats.save()
    response = redirect("characterMenu")

    return response
from django.shortcuts import redirect
from django.contrib import messages
from Login.models import Player
from .models import pStat

def getUserFromName(request):
    cookie = request.COOKIES.get('TheGameSessionID')
    if not (users := Player.objects.filter(userID=cookie)).exists():
        raise Exception('player does not exist')
    if not (userStats := pStat.objects.filter(username=users[0].username)).exists():
        raise Exception('player does not exist')
    return userStats[0]

def buyhealth(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    response = redirect("login")

    return response

def buyToughness(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    response = redirect("login")

    return response

def buyEvasion(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    response = redirect("login")

    return response
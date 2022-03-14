from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from Login.processes import getUserFromCookie
from TheGame.processes import getAllBosses, getUserFromName, getChampion
from Resources.processes import getAllUserResources

def homePageView(request):

    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')
    try:
        user = getUserFromCookie(request)
    except:
        return HttpResponseRedirect('login')

    resources = getAllUserResources(user)

    template = loader.get_template('TheGame/HomePage.html')
    context = {
        "user" : user, 
        "resources" : resources
    }
    output = template.render(context)

    return HttpResponse(output)

def characterMenu(request):

    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return HttpResponseRedirect('createChampion')

    template = loader.get_template('TheGame/CharacterMenu.html')
    context = {
    "username" : user.username,
    "pHealth" : champion.pHealth,
    "pToughness" : champion.pToughness,
    "pEvasion" : champion.pEvasion,
    "damage" : champion.damage,
    "accuracy" : champion.accuracy,
    "attackSpeed" : champion.attackSpeed,
    "aHealth" : champion.aHealth,
    "aToughness" : champion.aToughness,
    "aEvasion" : champion.aEvasion,
    }
    output = template.render(context, request)

    return HttpResponse(output)

def battleSelectView(request):
    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')
    
    user = getUserFromCookie(request)

    if not (champ := getChampion(user)):
        return HttpResponseRedirect('createChampion')

    user = getUserFromCookie(request)
    
    template = loader.get_template('TheGame/battleSelect.html')
    context = {}
    
    output = template.render(context, request)
    
    return HttpResponse(output)

def createChampionView(request):
    return HttpResponse("this is the champion create page")

def addNewBossView(request):
    user = getUserFromCookie(request)

    # if not user.role == "gameMaster":
    #     return HttpResponseRedirect('homePage')

    template = loader.get_template('TheGame/newBoss.html')

    bosses = getAllBosses()

    context = {
        "bosses" : bosses,
    }

    output = template.render(context, request)

    return HttpResponse(output)

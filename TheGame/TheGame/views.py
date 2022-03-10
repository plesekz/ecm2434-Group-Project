from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from Login.processes import getUserFromCookie
from TheGame.processes import getUserFromName
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
    userStats = getUserFromName(request)

    template = loader.get_template('TheGame/CharacterMenu.html')
    context = {
    "username" : user.username,
    "pHealth" : userStats.pHealth,
    "pToughness" : userStats.pToughness,
    "pEvasion" : userStats.pEvasion,
    "damage" : userStats.damage,
    "accuracy" : userStats.accuracy,
    "attackSpeed" : userStats.attackSpeed,
    "aHealth" : userStats.aHealth,
    "aToughness" : userStats.aToughness,
    "aEvasion" : userStats.aEvasion,
    }
    output = template.render(context, request)

    return HttpResponse(output)

def battleSelectView(request):
    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')
    
    user = getUserFromCookie(request)
    
    template = loader.get_template('TheGame/battleSelect.html')
    context = {}
    
    output = template.render(context, request)
    
    return HttpResponse(output)

def inventoryView(request : HttpRequest) -> HttpResponse:
    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')

    user = getUserFromCookie(request)
    userStats = getUserFromName(request)
    resources = getAllUserResources(user)

    template = loader.get_template('TheGame/CharacterViewer.html')
    context = {
        "user" : user,
        "stats": userStats,
        "resources": resources
    }

    output = template.render(context, request)

    return HttpResponse(output)
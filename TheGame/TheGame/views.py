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

def homePageView2(request : HttpRequest) -> HttpResponse:
    if not 'TheGameSessionID' in request.COOKIES.keys():
        return HttpResponseRedirect('/login')

    try:
        user = getUserFromCookie(request)
        stats = getUserFromName(request)
        resources = getAllUserResources(user)
    except:
        return HttpResponseRedirect('/login')

    template = loader.get_template('TheGame/HomePage2.html')
    context = {
        "user" : user,
        "stats": stats,
        "resources": resources
    }

    output = template.render(context, request)

    return HttpResponse(output)

def characterMenu2(request : HttpRequest) -> HttpResponse:
    if not 'TheGameSessionID' in request.COOKIES.keys():
        return HttpResponseRedirect('/login')

    try:
        user = getUserFromCookie(request)
        stats = getUserFromName(request)
        resources = getAllUserResources(user)
    except:
        return HttpResponseRedirect('/login')

    template = loader.get_template('TheGame/CharacterMenu2.html')
    context = {
        "user" : user,
        "stats" : stats,
        "resources" : resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)

def battleSelectView2(request : HttpRequest) -> HttpResponse:
    if not 'TheGameSessionID' in request.COOKIES.keys():
        return HttpResponseRedirect('/login')

    try:
        user = getUserFromCookie(request)
        stats = getUserFromName(request)
        resources = getAllUserResources(user)
    except:
        return HttpResponseRedirect('/login')

    template = loader.get_template('TheGame/battleSelect2.html')
    context = {
        "user" : user,
        "stats" : stats,
        "resources" : resources
    }

    output = template.render(context, request)

    return HttpResponse(output)


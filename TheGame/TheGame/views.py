from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from Login.processes import getUserFromCookie
from TheGame.processes import getUserFromName

def homePageView(request):

    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')

    user = getUserFromCookie(request)

    template = loader.get_template('TheGame/HomePage.html')
    context = {"userID" : user.pk}
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
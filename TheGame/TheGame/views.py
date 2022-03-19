from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from Login.processes import getUserFromCookie
from TheGame.processes import getAllBosses, getUserFromName, getChampion
from Resources.processes import getAllUserResources

def homePageView(request : HttpRequest) -> HttpResponse:
    """ creates response for the Home page
    """
    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')
      
    try:
        user = getUserFromCookie(request)
        champion = getChampion(user)
        resources = getAllUserResources(user)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/login')

    template = loader.get_template('TheGame/HomePage.html')
    context = {
        "user" : user,
        "champion": champion,
        "resources": resources
    }

    output = template.render(context, request)

    return HttpResponse(output)

def characterMenu(request : HttpRequest) -> HttpResponse:
    """ creates response for the character menu
    """
    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return HttpResponseRedirect('createChampion')

    template = loader.get_template('TheGame/CharacterMenu.html')

    resources = getAllUserResources(user)

    context = {
        "username" : user.username,
        "champion" : champion,
        "resources" : resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)

def battleSelectView(request : HttpRequest) -> HttpResponse:
    """ create response for the battle selection page
    """
    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')
    
    user = getUserFromCookie(request)

    if not (champ := getChampion(user)):
        return HttpResponseRedirect('createChampion')

    resources = getAllUserResources(user)

    bosses = getAllBosses()
    
    template = loader.get_template('TheGame/battleSelect.html')
    context = {
        "user" : user,
        "champion" : champ,
        "resources" : resources,
        "bosses" : bosses
    }

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

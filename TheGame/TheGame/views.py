from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from Login.processes import getUserFromCookie
from TheGame.processes import getUserFromName
from Resources.processes import getAllUserResources

def homePageView(request : HttpRequest) -> HttpResponse:
    """ creates response for the Home page
    """
    if not 'TheGameSessionID' in request.COOKIES.keys():
        return HttpResponseRedirect('/login')
      
    try:
        user = getUserFromCookie(request)
        stats = getUserFromName(request)
        resources = getAllUserResources(user)
    except:
        return HttpResponseRedirect('/login')

    template = loader.get_template('TheGame/HomePage.html')
    context = {
        "user" : user,
        "stats": stats,
        "resources": resources
    }

    output = template.render(context, request)

    return HttpResponse(output)

def characterMenu(request : HttpRequest) -> HttpResponse:
    """ creates response for the character menu
    """
    if not 'TheGameSessionID' in request.COOKIES.keys():
        return HttpResponseRedirect('/login')
      
    try:
        user = getUserFromCookie(request)
        stats = getUserFromName(request)
        resources = getAllUserResources(user)
    except:
        return HttpResponseRedirect('/login')

    template = loader.get_template('TheGame/CharacterMenu.html')
    context = {
        "user" : user,
        "stats" : stats,
        "resources" : resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)

def battleSelectView(request : HttpRequest) -> HttpResponse:
    """ create response for the battle selection page
    """
    if not 'TheGameSessionID' in request.COOKIES.keys():
        return HttpResponseRedirect('/login')

    try:
        user = getUserFromCookie(request)
        stats = getUserFromName(request)
        resources = getAllUserResources(user)
    except:
        return HttpResponseRedirect('/login')

    template = loader.get_template('TheGame/battleSelect.html')
    context = {
        "user" : user,
        "stats" : stats,
        "resources" : resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)


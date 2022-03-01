from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from Login.processes import getUserFromCookie
from Resources.processes import getAllUserResources

def homePageView(request):

    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')

    user = getUserFromCookie(request)
    resources = getAllUserResources(user)

    template = loader.get_template('TheGame/HomePage.html')
    context = {
        "user" : user, 
        "resources" : resources
    }
    output = template.render(context)

    return HttpResponse(output)
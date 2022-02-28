from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from Login.processes import getUserFromCookie

def homePageView(request):

    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')

    user = getUserFromCookie(request)

    template = loader.get_template('TheGame/HomePage.html')
    context = {"userID" : user.pk}
    output = template.render(context)

    return HttpResponse(output)
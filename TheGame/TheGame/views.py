from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from Login.processes import getUserPkFromCookie

def homePageView(request):

    if request.COOKIES.get('TheGameSessionID') == None:
        return HttpResponseRedirect('login')

    uid = getUserPkFromCookie(request)

    print (uid)

    template = loader.get_template('TheGame/HomePage.html')
    context = {"userID" : uid}
    output = template.render(context)

    return HttpResponse(output)
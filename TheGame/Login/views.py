from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.messages import get_messages

def indexPage(request):
    template = loader.get_template("Login/index.html")

    context = {}

    output = template.render(context, request)

    return HttpResponse(output)

def loginPage(request):
    template = loader.get_template("Login/loginPage.html")

    #messages = get_messages(request)

    context = {}

    # for mess in messages:
    #     print(mess)

    output = template.render(context, request)

    return HttpResponse(output)

def registerPage(request):
    template = loader.get_template("Login/registerPage.html")

    context = {}

    output = template.render(context, request)

    return HttpResponse(output)
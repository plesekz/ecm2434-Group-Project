from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.messages import get_messages
from Login.models import Player
from django.contrib import messages
from django.shortcuts import redirect


def indexPage(request):
    template = loader.get_template("Login/index.html")

    context = {}

    output = template.render(context, request)

    return HttpResponse(output)


def loginPage(request):
    template = loader.get_template("Login/loginPage.html")
    current_cookie = request.COOKIES.get('TheGameSessionID')
    if Player.objects.filter(userID=current_cookie).exists():
        messages.success(request, ('Logged in'))
        response = redirect("homePage")

    context = {}

    output = template.render(context, request)

    return HttpResponse(output)


def registerPage(request):
    template = loader.get_template("Login/registerPage.html")

    context = {}

    output = template.render(context, request)

    return HttpResponse(output)

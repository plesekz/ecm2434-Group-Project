from email.message import EmailMessage
from django.shortcuts import redirect
from .forms import PlayerForm
from .models import Player
from django.contrib import messages
from django.contrib.auth import authenticate

def validateLogIn(request):
    if not request.method == "POST":
        messages.success(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    _email = request.POST['email']
    _username = request.POST['username']
    _password = request.POST['password']

    if Player.objects.filter(email=_email).exists():
        user = authenticate(request, username=_username, password=_password)
        if user is not None:
            response = redirect("login")
            response.set_cookie('TheGameSessionID', 'cookie_value')
        else:
            messages.success(request, ('Incorrect password, try again'))
    else:
        messages.success(request, ('Username entered doesn\'t exist'))

    #proccess log in

    return response

def validateRegister(request):
    if not request.method == "POST":
        messages.success(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    form = PlayerForm(request.POST or None)

    email = request.POST['email']
    #password = request.POST['password']
    username = request.POST['username']

    if Player.objects.filter(email=email).exists():
        messages.success(request, ('The Email you chose is taken'))
        return redirect("register")
    if Player.objects.filter(username=username).exists():
        messages.success(request, ('The Username you chose is taken'))
        return redirect("register")

    if form.is_valid():
        form.save()


    #proccess registration
    messages.success(request, ('Successfully registered'))
    return redirect("login")
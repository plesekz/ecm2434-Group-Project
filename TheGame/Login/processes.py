from email.message import EmailMessage
from http.client import HTTPResponse
from django.shortcuts import redirect
from Login.forms import PlayerForm
from Login.models import Player
from django.contrib import messages
from django.db.models import Q

def validateLogIn(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    _email = request.POST['email']
    _username = request.POST['email']
    _password = request.POST['password']

    response = redirect("login")

    if Player.objects.filter(email=_email).exists() or Player.objects.filter(username=_username).exists():
        #user = authenticate(username=_username, password=_password)
        query = ((Q(username=_username) | Q(email=_email)) & Q(password=_password))
        user = Player.objects.get(query)
        
        if user is not None:
            messages.success(request, ('Logged in'))
            response = redirect("login")
            response.set_cookie('TheGameSessionID', 'cookie_value')
        else:
            messages.warning(request, ('Incorrect password, try again'))
    else:
        messages.warning(request, ('Username entered doesn\'t exist'))
        response = redirect("login")

    #proccess log in

    return response

def validateRegister(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        #return "failed to process, please use POST method"
        return redirect("register")
    form = PlayerForm(request.POST or None)

    email = request.POST['email']
    #password = request.POST['password']
    username = request.POST['username']

    if Player.objects.filter(email=email).exists():
        messages.warning(request, ('The Email you chose is taken'))
        return redirect("register")
    if Player.objects.filter(username=username).exists():
        messages.warning(request, ('The Username you chose is taken'))
        return redirect("register")

    if not form.is_valid():
        messages.error(request, ('Something went wrong please try again'))
        return redirect("register")
    
    form.save()

    #proccess registration
    messages.success(request, ('Successfully registered'))
    return redirect("login")
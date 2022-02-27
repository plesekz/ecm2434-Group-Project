import time
from django.shortcuts import redirect
from Login.forms import PlayerForm
from Login.models import Player
from django.contrib import messages
from django.db.models import Q
import hashlib

def validateLogIn(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    _email = request.POST['email']
    _username = request.POST['email']
    _password = hashlib.sha256(request.POST['password'].encode()).hexdigest()
    response = redirect("login")

    if Player.objects.filter(email=_email).exists() or Player.objects.filter(username=_username).exists():
        try:
            query = ((Q(username=_username) | Q(email=_email)) & Q(password=_password))
            user = Player.objects.get(query)
            if user is not None:
                messages.success(request, ('Logged in'))
                response = redirect("login")
                cookie = bake_cookie(_username)
                response.set_cookie('TheGameSessionID', cookie)
                user.userID = cookie
                user.save()
        except Exception as e:
            messages.warning(request, ('Incorrect password, try again'))
    else:
        messages.warning(request, ('Username or email entered doesn\'t exist'))

    return response

def validateRegister(request):
    response = redirect("register")
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        #return "failed to process, please use POST method"
        return response

    _email = request.POST['email']
    _password = hashlib.sha256(request.POST['password'].encode()).hexdigest()
    _username = request.POST['username']
    if Player.objects.filter(email=_email).exists():
        messages.warning(request, ('The Email you chose is taken'))
        return response
    if Player.objects.filter(username=_username).exists():
        messages.warning(request, ('The Username you chose is taken'))
        return response

    cookie = bake_cookie(_username)
    form = Player(email=_email, username=_username, password=_password, userID=cookie)

    response.set_cookie('TheGameSessionID', cookie)

    form.save()
    response = redirect("login")
    messages.success(request, ('Successfully registered'))
    return response

def bake_cookie(usrname):
    cookie = hashlib.sha256((usrname +''+ str(time.time())).encode()).hexdigest()
    return cookie

def is_game_master(cookie):
    try:
        query = (Q(userID=cookie) & Q(role='GM'))
        user = Player.objects.get(query)
        if user is not None:
            return True
    except Exception as e:
        return False
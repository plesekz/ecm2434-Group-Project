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
                response.set_cookie('TheGameSessionID', 'cookie_value')
        except Exception as e:
            messages.warning(request, ('Incorrect password, try again'))
            response = redirect("login")
    else:
        messages.warning(request, ('Username entered doesn\'t exist'))
        response = redirect("login")

    return response

def validateRegister(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        #return "failed to process, please use POST method"
        return redirect("register")

    _email = request.POST['email']
    #request.POST['password'] = hashlib.sha256(request.POST['password'].encode()).hexdigest()
    _username = request.POST['username']
    form = Player(email=request.POST['email'], username=request.POST['username'], password=hashlib.sha256(request.POST['password'].encode()).hexdigest())
    

    if Player.objects.filter(email=_email).exists():
        messages.warning(request, ('The Email you chose is taken'))
        return redirect("register")
    if Player.objects.filter(username=_username).exists():
        messages.warning(request, ('The Username you chose is taken'))
        return redirect("register")

    #if not form.is_valid():
    #    messages.error(request, ('Something went wrong please try again'))
    #    return redirect("register")
    
    form.save()

    #proccess registration
    messages.success(request, ('Successfully registered'))
    return redirect("login")
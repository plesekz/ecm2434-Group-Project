from django.shortcuts import redirect
from .forms import PlayerForm
from .models import Player
from django.contrib import messages

def validateLogIn(request):
    if not request.method == "POST":
        return "failed to process, please use POST method"

    email = request.POST['email']
    password = request.POST['password']

    #proccess log in

    response = redirect("login")
    response.set_cookie('cookie_name', 'cookie_value')


    return response

def validateRegister(request):
    if not request.method == "POST":
        return "failed to process, please use POST method"
    form = PlayerForm(request.POST or None)

    email = request.POST['email']
    #password = request.POST['password']
    username = request.POST['username']

    if Player.objects.filter(email=email).exists():
        return redirect("register")#return "Email is taken"
    if Player.objects.filter(username=username).exists():
        return redirect("register")#return "Username is taken"

    if form.is_valid():
        form.save()


    #proccess registration
    messages.success(request, ('Successfully registered'))
    return redirect("login")
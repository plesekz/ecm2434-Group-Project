from django.shortcuts import redirect

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

    email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']

    #proccess registration

    return redirect("login")
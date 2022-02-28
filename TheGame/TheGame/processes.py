from django.shortcuts import redirect
from django.contrib import messages

def buyhealth(request):
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    response = redirect("CharacterMenu")

    return response
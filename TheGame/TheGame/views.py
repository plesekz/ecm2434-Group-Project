from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def loginPage(request):
    template = loader.get_template("TheGame/loginPage.html")

    context = {}

    output = template.render(context, request)

    return HttpResponse(output)
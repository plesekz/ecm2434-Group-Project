from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.

def QR_management(request):
    codes = get_object_or_404(PLACEHOLDER_FOR_CODES)
    list_of_resources = get_object_or_404(PLACEHOLDER_FOR_ALL_RESOURCE_TYPES_IN_THE_RESOURCE_MANAGEMENT_MODULE)
    dict = {
        "codes" : codes,
        "list_of_resources" : list_of_resources
    }
    return render(request, 'QRC/manage.html', dict)

def qr_landing(request):
    template = loader.get_template("QRC/landing.html")
    output = template.render({}, request)
    return HttpResponse(output)
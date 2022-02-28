from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.

#def QR_management(request):
#    codes = get_object_or_404(PLACEHOLDER_FOR_CODES)
#    return render(request, 'QRC/manage.html', codes)

def qr_landing(request):
    template = loader.get_template("QRC/landing.html")
    output = template.render({}, request)
    return HttpResponse(output)
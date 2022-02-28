from django.shortcuts import render

# Create your views here.

def QR_management(request):
    codes = get_object_or_404(PLACEHOLDER_FOR_CODES)
    return render(request, 'QRC/manage.html', codes)
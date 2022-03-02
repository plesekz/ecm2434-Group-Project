from Resources.models import Resource
from Resources.processes import addResourceToUser
from Login.processes import getUserFromCookie
from QRC.models import QRResource, QRC
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import json


def createRes(request):
    data = request.body.decode('utf-8')  # Python decodes from bytestring to str
    json_data = json.loads(data)
    QRID = json_data['codeID']
    # QRC.objects.create(QRID=json_data.codeID, latitude=json_data.latitude, longitude=json_data.longitude)
    QRC.objects.create(QRID=QRID, latitude=json_data['latitude'], longitude=json_data['longitude'])
    for resource in json_data.res1type:  # for each resource type within the QR code, create a new QRResource
        if not (resource := Resource.objects.filter(id=json_data['res1type'][resource])).exists():
            return HttpResponse(status=500) # The resource that's being added does not exist in the database
        QRResource.objects.create(QRID_id=QRID, amount=json_data['amount'], resource_id=resource[0].id)
    return HttpResponse(status=200)



def deleteRes(request):
    UID = int(request.GET['data'])
    qrCode = QRC.objects.get(QRID=UID)
    if not (qrresources := QRResource.objects.filter(QRID=qrCode)).exists():
        return HttpResponse(status=201) # A QRResource with the given UID doesn't exist so already 'deleted'
    for qrres in qrresources:
        qrres.delete()
    return HttpResponse(status=200)


def retrieveRes(request):
    UID = request.GET['data']
    # resource = get_object_or_404(Resource.objects.filter(name=UID))[0]

    qrCode = QRC.objects.get(QRID=UID)

    if not (qrResources := QRResource.objects.filter(QRID=qrCode)).exists():
        return HttpResponse(status=501) # A QRResource with the given UID doesn't exist

    user = getUserFromCookie(request)
    try:
        for qrResource in qrResources:
            addResourceToUser(user, qrResource.resource, qrResource.amount)
    except Exception as e:
        print(e)
        return HttpResponse(status=502) # Failed to add resource to user
    return HttpResponse(status=200)


def listRes(request):
    querySet = QRC.objects.all()
    listOfQRs = []
    for qrc in querySet:
        qrResources = QRResource.objects.filter(QRID_id=qrc.QRID)
        resourceList = []
        jsonString = '{"codeID":"value1","res1Type":"value2","resource1Amount":"value3", "latitude":"value4", ' \
                     'longitude":"value5"} '
        jsonString['codeID'] = qrc.QRID
        jsonString['resource1Amount'] = qrResources[0].amount
        jsonString['latitude'] = qrc.latitude
        jsonString['longitude'] = qrc.longitude
        for qrResource in qrResources:
            resourceList.append(qrResource.resource)
        jsonString['res1Type'] = "{" + ', '.join(resourceList) + "}"

        listOfQRs.append(jsonString)
    return HttpResponse(listOfQRs)

# Create your views here.

def QR_management(request):
    codes = []
    for QRCode in QRC.objects.all():
        codes.append(
            {
                'name': QRCode.QRID,
                'lat': QRCode.latitude,
                'lon': QRCode.longitude,
                'resources': QRResource.objects.filter(QRID=QRCode.QRID)
            }
        ) 
    list_of_resources = Resource.objects.all()
    dict = {
        "codes" : codes,
        "list_of_resources" : list_of_resources
    }
    return render(request, 'QRC/manage.html', dict)

def qr_landing(request):
    template = loader.get_template("QRC/landing.html")
    output = template.render({}, request)
    return HttpResponse(output)

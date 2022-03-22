from Resources.models import Resource
from Resources.processes import addResourceToUser
from Login.processes import getUserFromCookie
from QRC.models import QRResource, QRC
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
import json
import qrcode
import os


def createRes(request: HttpRequest) -> HttpResponse:
    """ function that takes a http request with json body and creates a qr code with an associated resource\n
    Args:
        request(HttpRequest): POST request containing json body with details about a new qrCode
    returns:
        HttpResponse: response with status code
        200: success
        500: resource does not exist
    """

    data = request.body.decode('utf-8')  # decode the body to a string
    json_data = json.loads(data)  # load json from string data

    qrid = json_data['codeID']

    # make sure the resource exists
    try:
        res = Resource.objects.get(pk=int(json_data['res1Type']))
    except Resource.DoesNotExist:
        return HttpResponse(status=500)

    # if qr code exists then use that one else create a new one
    if (qrcs := QRC.objects.filter(QRID=qrid)).exists():
        qrc = qrcs[0]
    else:
        # generate a new qr code
        data = json_data['codeID']

        qr = qrcode.QRCode(
            box_size=15,
            border=5
        )

        qr.add_data(data)
        qr.make(fit=True)

        qrImage = qr.make_image(fill="black", back_color="white")
        filepath = f"QRC/qrImages/{json_data['codeID']}.png"
        filedirectorypath = "QRC/static/QRC/qrImages/"
        if not os.path.exists(filedirectorypath):
            os.makedirs(filedirectorypath)
        qrImage.save("QRC/static/" + filepath)

        try:
            latitude = '{:06.4f}'.format(float(json_data['longitude']))
            longitude = '{:06.4f}'.format(float(json_data['longitude']))
        except ValueError:
            print("bru")

        qrc = QRC.objects.create(
            QRID=int(json_data['codeID']),
            latitude=latitude,
            longitude=longitude,
            image=filepath
        )

    # if that resource is already on that qr then update else create a new
    # entry
    if (qrr := QRResource.objects.filter(QRID=qrc, resource=res)).exists():
        qrr[0].amount = int(json_data['resource1Amount'])
    else:
        qrr = QRResource.objects.create(
            QRID=qrc, resource=res, amount=int(
                json_data['resource1Amount']))

    qrc.save()
    qrr.save()
    return HttpResponse(status=200)


def deleteRes(request: HttpRequest) -> HttpResponse:
    """ function that recieves an http request containing the QRID of a qr code and removes that qr code from the system\n
    Args:
        request(HttpRequest): POST request containing a QRID in the body
    Returns:
        HttpResponse: response with status code:
            200: success
            201: no resource with QRID exists
    """
    qrid = int(request.body)
    qrCode = QRC.objects.get(QRID=qrid)
    if not (qrresources := QRResource.objects.filter(QRID=qrCode)).exists():
        QRC.objects.get(QRID=qrid).delete()
        # delete image
        os.remove(f"QRC/static/QRC/qrImages/{qrid}.png")
        # A QRResource with the given UID doesn't exist so already 'deleted'
        return HttpResponse(status=201)
    for qrres in qrresources:
        qrres.delete()
    return HttpResponse(status=200)


def retrieveRes(request: HttpRequest) -> HttpResponse:
    """function that takes HttpRequest with qr code and adds associated resources to user\n
    Args:
        request(HttpRequest): GET request with QRID in the url
    Returns:
        HttpResponse: HttpResponse with request, also contains json on success
        200: success, returns json object
        501: QRC does not exist, or has no resources associated
        502: failed to add resources to user
    """
    UID = request.GET['data']
    # resource = get_object_or_404(Resource.objects.filter(name=UID))[0]

    try:
        qrCode = QRC.objects.get(QRID=UID)
    except QRC.DoesNotExist:
        return HttpResponse(status=501)

    if not (qrResources := QRResource.objects.filter(QRID=qrCode)).exists():
        # A QRResource with the given UID doesn't exist
        return HttpResponse(status=501)

    user = getUserFromCookie(request)
    output = []
    try:
        for qrResource in qrResources:
            addResourceToUser(user, qrResource.resource, qrResource.amount)
            output.append([str(qrResource.resource), qrResource.amount])
    except Exception as e:
        print(e)
        return HttpResponse(status=502)  # Failed to add resource to user
    return HttpResponse(json.dumps(output), status=200)


def listRes(request: HttpRequest) -> HttpResponse:
    """function that returns json objects of all qr codes and their associated resources\n
    Args:
        request(HttpRequest): httpRequest
    Returns:
        HttpResponse: response containing json with all qr codes and their associated resources
    """
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


def QR_management(request: HttpRequest) -> HttpResponse:
    """ function that returns rendered temlpate for QR management page\n
    Args:
        request(HttpRequest): HttpRequest
    Returns:
        HttpResponse: response containing html generated by template
    """
    codes = []
    for QRCode in QRC.objects.all():
        codes.append(
            {
                'name': QRCode.QRID,
                'lat': QRCode.latitude,
                'lon': QRCode.longitude,
                'resources': QRResource.objects.filter(QRID=QRCode),
                'imagePath': QRCode.image,
                'staticPath': "QRC/qrImages/"
            }
        )
    list_of_resources = Resource.objects.all()
    dict = {
        "active_QR_codes_list": codes,
        "list_of_resources": list_of_resources
    }
    return render(request, 'QRC/manage.html', dict)


def qr_landing(request: HttpRequest) -> HttpResponse:
    """ function that returns rendered template for qr landing page
    Args:
        request(HttpRequest): httpRequest
    Returns:
        HttpResponse: response containing html generated by template
    """
    template = loader.get_template("QRC/landing.html")
    output = template.render({}, request)
    return HttpResponse(output)

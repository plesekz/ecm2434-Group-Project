from django.http import HttpResponse, HttpResponseRedirect
from QRC.models import Resource
from django.db.models import JSONField
import json


def createRes(request):
    resource = JSONField
    data = request.body.decode('utf-8')  # Python decodes from bytestring to str
    json_data = json.loads(data)
    Resource.objects.create(
        codeID=json_data.codeID,
        #Need to add more
    )


def deleteRes(request):
    pass


def retrieveRes(request):
    pass


def listRes(request):
    pass

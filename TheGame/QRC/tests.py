from email import header
from time import sleep
from django.test import TestCase, Client
from QRC.models import QRC, QRResource
from Resources.models import Resource, PlayerResource
from Resources.processes import getAllUserResources
from http.cookies import SimpleCookie
from Login.models import Player
import json

# Create your tests here.

class QrTestCase(TestCase):
    def setUp(self):
        self.qr1 = QRC.objects.create(
            QRID = 1234,
            latitude = 12.4567,
            longitude = 23.5678,
        )

        self.res1 = Resource.objects.create(
            name="wood"
        )

        self.res2 = Resource.objects.create(
            name="stone"
        )

        self.qrToDelete = QRC.objects.create(
            QRID = 9876,
            latitude = 12.4567,
            longitude = 23.5678,
        )

        QRResource.objects.create(
            QRID=self.qrToDelete,
            amount=12,
            resource=self.res1,
        )

        QRResource.objects.create(
            QRID=self.qrToDelete,
            amount=121,
            resource=self.res1,
        )



    def test_qrc_constraints(self):
        """ tests to make sure you cant make invlaid qr codes
        """
        # test invalid QRID
        try:
            newQrCode = QRC.objects.create(
                QRID = -7654321,
                latitude = 21.3467,
                longitude = 14.6753,
            )
            assert False
        except:
            assert True
        
        # test invalid latitude
        try:
            newQrCode = QRC.objects.create(
                QRID = 7654321,
                latitude = 212.3467653,
                longitude = 14.6753,
            )
            assert False
        except:
            assert True
        
        # test invalid longitude
        try:
            newQrCode = QRC.objects.create(
                QRID = 7654321,
                latitude = 21.3467,
                longitude = 14.6753,
            )
            assert False
        except:
            assert True

    def test_creating_qr_resource_link(self):
        """ tests to make sure that adding resources to qr codes is
        functioning correctly
        """

        # add the resources to the qr code

        QRResource.objects.create(
            QRID=self.qr1,
            resource = self.res1,
            amount = 12,
        )
        
        QRResource.objects.create(
            QRID=self.qr1,
            resource = self.res2,
            amount = 5,
        )

        # check that the resources have been assigned properly
        
        # check that the amount of resources associated with
        # the qr code is correct
        qrr_set = self.qr1.qrresource_set.all()
        self.assertEquals(len(qrr_set), 2)

        # check that each resource was given the right amount
        # of resource
        qrr = QRResource.objects.get(
            QRID=self.qr1, resource=self.res1,
        )

        self.assertEquals(qrr.amount, 12)
        
        qrr = QRResource.objects.get(
            QRID=self.qr1, resource=self.res2,
        )

        self.assertEquals(qrr.amount, 5)

    def test_create_resource(self):
        """ function that tests creating resources
        """

        c = Client()

        # request to make a qr code and add 65 wood to it
        res = c.post("/qr/createRes",
            json.dumps({
                'codeID': '56743',
                'latitude': '34.5442',
                'longitude': '42.2563',
                'res1Type': '1',
                'resource1Amount': '65'
            }),
            content_type='application/json'
            
        )

        # this should have made and entry in the qrResource database
        # that has the qrCode and the resource linked together

        try:
            #get the qrCode
            qrc = QRC.objects.get(QRID=56743)
            qrr = QRResource.objects.get(QRID=qrc, resource_id=1)
            assert True
        except:
            assert False

    def test_delete_resource(self):
        """ function to test deleting resources
        """

        """ this unit test currently doesnt work because
        password is hashed before being checked so we have to
        change the players password to a hashed version of the password
        """

        pToLogIn = Player.objects.create(
            userID = 0,
            role = "placeHolder",
            email="testing@email.com",
            username="testingUsername",
            password="testingPassword", #this has be to changeed to a hash
        )

        # qrid of qr to test deleting is 9876

        c = Client()

        res = c.post('/qr/deleteRes',
            json.dumps(9876),
            content_type='application/json'
        )

        # qr should now have no resources

        assert not QRResource.objects.filter(QRID_id=9876).exists()

        # now we send the same request and it should delete the qr code from the system
        # as there are no associated resources

        res = c.post('/qr/deleteRes',
            json.dumps(9876),
            content_type='application/json'
        )

        assert not QRResource.objects.filter(QRID=9876).exists()

    def test_retrieve_resource(self):

        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        
        #log in a player and get the cookie

        res = c.post('/login/ValidateLogin/',
            {
                'email': spToLogIn.email,
                'password': "testingPassword",
            }
        )

        c = res.client

        assert res.status_code < 400
        # create a new qr and resource

        qr = QRC.objects.create(
            QRID = 5678,
            latitude = 12.4567,
            longitude = 23.5678,
        )
        
        QRResource.objects.create(
            QRID=qr,
            resource=self.res1,
            amount=200,
        )

        # now the user should have the right cookies to request resources
        url = f"/qr/retrieveRes/?data={qr.QRID}"
        res = c.get(url)

        print(res.status_code)

        assert res.status_code < 400

        #check that the user has got the 200 wood

        assert PlayerResource.objects.filter(player=pToLogIn, resource=self.res1).exists()
        assert (self.res1, 200) in getAllUserResources(pToLogIn)


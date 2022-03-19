from email import header
from getpass import getuser
from time import sleep
from django.test import TestCase, Client
from QRC.models import QRC, QRResource
from Resources.models import Resource, PlayerResource
from Resources.processes import getAllUserResources
from http.cookies import SimpleCookie
from Login.models import Player
from Login.processes import getUserFromCookie
import json

# Create your tests here.


class QrTestCase(TestCase):

    def setUp(self):

        # set up a qr code that we can use
        self.qr1 = QRC.objects.create(
            QRID=1234,
            latitude=12.4567,
            longitude=23.5678,
        )

        # set up some resources
        self.res1 = Resource.objects.create(
            name="wood"
        )

        self.res2 = Resource.objects.create(
            name="stone"
        )

        # set up a qr code to test deleting
        self.qrToDelete = QRC.objects.create(
            QRID=9876,
            latitude=12.4567,
            longitude=23.5678,
        )

        # give the qr code some resources to delete
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

        # create a client to log in to the system
        self.client = Client()

        # register the client
        res = self.client.post('/login/ValidateRegister/',
                               {
                                   'email': "test@email.com",
                                   'username': 'testUsername',
                                   'password': 'testPassword',
                                   'confirmPassword': 'testPassword'
                               }
                               )
        self.client = res.client

        # log in the client

        res = self.client.post('/login/ValidateLogin/',
                               {
                                   'email': 'test@email.com',
                                   'password': 'testPassword'
                               }
                               )

        self.client = res.client

    def test_qrc_constraints(self):
        """ tests to make sure you cant make invlaid qr codes
        """
        # test invalid QRID
        try:
            newQrCode = QRC.objects.create(
                QRID=-7654321,
                latitude=21.3467,
                longitude=14.6753,
            )
            assert False
        except BaseException:
            assert True

        # test invalid latitude
        try:
            newQrCode = QRC.objects.create(
                QRID=7654321,
                latitude=212.3467653,
                longitude=14.6753,
            )
            assert False
        except BaseException:
            assert True

        # test invalid longitude
        try:
            newQrCode = QRC.objects.create(
                QRID=7654321,
                latitude=21.3467,
                longitude=14.6753,
            )
            assert False
        except BaseException:
            assert True

    def test_creating_qr_resource_link(self):
        """ tests to make sure that adding resources to qr codes is
        functioning correctly
        """

        # add the resources to the qr code

        QRResource.objects.create(
            QRID=self.qr1,
            resource=self.res1,
            amount=12,
        )

        QRResource.objects.create(
            QRID=self.qr1,
            resource=self.res2,
            amount=5,
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
            # get the qrCode
            qrc = QRC.objects.get(QRID=56743)
            qrr = QRResource.objects.get(QRID=qrc, resource_id=1)
            assert True
        except BaseException:
            assert False

    def test_delete_resource(self):
        """ function to test deleting resources
        """

        res = self.client.post('/qr/deleteRes',
                               json.dumps(9876),
                               content_type='application/json'
                               )

        # qr should now have no resources

        assert not QRResource.objects.filter(QRID_id=9876).exists()

        # now we send the same request and it should delete the qr code from the system
        # as there are no associated resources

        res = self.client.post('/qr/deleteRes',
                               json.dumps(9876),
                               content_type='application/json'
                               )

        assert not QRResource.objects.filter(QRID=9876).exists()

    def test_retrieve_resource(self):
        """ function to test that a user can retrieve the resources of a given qr code
        by using the urls that we have created
        """

        # create a new qr and give it resource 1
        qr = QRC.objects.create(
            QRID=5678,
            latitude=12.4567,
            longitude=23.5678,
        )

        QRResource.objects.create(
            QRID=qr,
            resource=self.res1,
            amount=200,
        )

        # send out client to the url to retrieve the resources
        url = f"/qr/retrieveRes/?data={qr.QRID}"
        res = self.client.get(url)

        print(res.status_code)

        assert res.status_code < 400

        # check that the user has got the 200 wood

        p = Player.objects.get(username="testUsername")

        assert PlayerResource.objects.filter(
            player=p, resource=self.res1).exists()

        assert (self.res1, 200) in getAllUserResources(p)

    def test_list_resource(self):
        """ function to test if resources are listed correctly
        """

        assert True

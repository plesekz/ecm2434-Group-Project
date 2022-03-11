from django.test import TestCase
from QRC.models import QRC, QRResource
from Resources.models import Resource

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
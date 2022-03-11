from django.test import TestCase
from QRC.models import QRC, QRResource

# Create your tests here.

class QrTestCase(TestCase):
    def setUp(self):
        self.qr1 = QRC.objects.create(
            QRID = 1234,
            latitude = 12.4567,
            longitude = 23.5678,
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

    
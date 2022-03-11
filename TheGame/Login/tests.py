from django.test import TestCase
from Login.models import Player

class LoginTestCase(TestCase):

    def setUp(self):
        self.p1 = Player.objects.create(
            
        )

    def test_():
        assert False
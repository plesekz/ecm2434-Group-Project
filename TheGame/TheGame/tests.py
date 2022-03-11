from django.test import TestCase
from TheGame.models import pStat
from Login.models import Player

class TheGameTestCase(TestCase):
    def setUp(self):
        self.p1 = Player.objects.create(
            userID=0,
            role="placeHolder",
            email="placeholder@email.com",
            password="passWrd",
        )

    def test_(self):
        assert True
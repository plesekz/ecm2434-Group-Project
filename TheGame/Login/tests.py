from time import sleep
from django.http import HttpRequest
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from Login.models import Player
from Login.processes import validateRegister
import requests
import json

class LoginTestCase(TestCase):

    def setUp(self):
        return None

    def test_registration(self):

        client = Client()
        # send a request to the validate login page
        client.post(
            "/login/validateRegister/",
            data={
                'email' : "test@email.com",
                'username' : "testUsername",
                'password': "testPassword",
                'confirmPassword' : "testPassword"
            },
            content_type='application/json'
        )

        #check that the user was added to the database
        sleep(2)

        try:
            user = Player.objects.get(username="testUsername")
            assert True
        except:
            assert False
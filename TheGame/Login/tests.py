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
        response = client.post(
            "/login/ValidateRegister/",
            {
                'email' : "test@email.com",
                'username' : "testUsername",
                'password': "testPassword",
                'confirmPassword' : "testPassword"
            },
        )
        #check that the user was added to the database

        try:
            user = Player.objects.get(username="testUsername")
            assert True
        except:
            assert False
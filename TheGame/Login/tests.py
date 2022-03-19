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

    def test_registration_and_login(self):

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

        client = response.client

        try:
            user = Player.objects.get(username="testUsername")
            assert True
        except:
            assert False

        # test that we can log in to the system

        response = client.post('/login/ValidateLogin/',
            {
                'email': "test@email.com",
                'password': 'testPassword'
            }
        )

        # check that the cookie was set to the right value
        client = response.client
        user = Player.objects.get(username="testUsername")

        self.assertEquals( user.userID , client.cookies.get('TheGameSessionID').value )

        
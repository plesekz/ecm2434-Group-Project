from django.test import TestCase
from Resources.models import Resource, PlayerResource
from Login.models import Player
from Resources.processes import *

# Create your tests here.
class ResourceTestCase(TestCase):
    
    def setUp(self):
        self.res1 = Resource.objects.create(name="wood")
        self.res2 = Resource.objects.create(name="stone")

        self.p1 = Player.objects.create(role="placeholder",
            email="dave@email.com",
            username="dave", password="placeholder")

        self.p2 = Player.objects.create(role="placeholder",
            email="dave@email.com",
            username="dave", password="placeholder")

    def test_resource_name_unique(self):
        """test to make sure that no 2 resources can have the same name
        """
        try:
            self.res5 = Resource.objects.create(name="wood")
            assert False
        except:
            assert True

    def test_adding_and_removing_resource_to_player(self):
        """function to test that resources are given to players correctly
        """

        addResourceToUser(self.p1, self.res1, 3) #add 3 wood to player 1
        
        #make a query to see how much wood player 1 has
        playerRes = PlayerResource.objects.get(player=self.p1, resource=self.res1)
        #assert that they have 3
        self.assertEquals(playerRes.amount, 3)

        # test that we can remove resources
        # remove 2 wood from player 1 who should have 3 wood
        removeResourceFromUser(self.p1, self.res1, 2)
        playerRes = PlayerResource.objects.get(player=self.p1, resource=self.res1)
        # assert tha the player has 1 left
        self.assertEquals(playerRes.amount, 1)

        # test that you cannot remove more resource than the player has
        # p1 should only have 1 so if we remove 5 it should throw an exception
        try:
            removeResourceFromUser(self.p1, self.res1, 5)
            assert False
        except:
            assert True

    def test_getting_resources(self):
        """ function to test functions that will get resources
        """

        # give the player some resources that we can use
        # 10 wood
        addResourceToUser(self.p2, self.res1, 10)
        # 15 stone
        addResourceToUser(self.p2, self.res2, 15)

        # get all the resources for the user
        resList = getAllUserResources(self.p2)

        # check the output is as expected, should be a list of tuples
        # each containing a resources and an amount
        self.assertEqual(resList, [(self.res1, 10), (self.res2, 15)] )

        # test that we can get a resource by its name
        resWood = getResourceByName("wood")
        # should return the wood resource
        self.assertEquals(resWood, self.res1)


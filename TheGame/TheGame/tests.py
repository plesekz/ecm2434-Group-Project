from django.test import TestCase, Client
from TheGame.models import pStat
from TheGame.processes import getUserFromName #this function gets the users stats
from Login.models import Player
from Resources.processes import addResourceToUser
from Resources.models import PlayerResource, Resource


class TheGameTestCase(TestCase):
    def setUp(self):
        self.p1 = Player.objects.create(
            userID=0,
            role="placeHolder",
            email="placeholder@email.com",
            password="passWrd",
        )
        
        # create a client to use in the tests
        self.client = Client()

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
        # get the object for the player that the client is logged in as
        self.pClient = Player.objects.get(username="testUsername")

        # create some resources
        self.res1 = Resource.objects.create(name="wood")
        self.res2 = Resource.objects.create(name="stone")        
        self.res3 = Resource.objects.create(name="iron")
        # give the player resources to spend on the upgrades
        addResourceToUser(self.pClient, self.res1, 100)
        addResourceToUser(self.pClient, self.res2, 100)
        addResourceToUser(self.pClient, self.res3, 100)
        


    def test_buy_phealth(self):

        # get the health before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startHealth = stats.pHealth
        #buy health
        res = self.client.post("/buyphealth/")
        assert res.status_code < 400
        # get the health after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endHealth = stats.pHealth
        # make sure health has increased by one
        self.assertEquals(startHealth + 1, endHealth)


    def test_buy_ptoughness(self):

        # get the toughness before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startTougness = stats.pToughness
        #buy toughness
        res = self.client.post("/buyptoughness/")
        assert res.status_code < 400
        # get the toughness after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endToughness = stats.pToughness
        # make sure toughness has increased by one
        self.assertEquals(startTougness + 1, endToughness)

    def test_buy_pevasion(self):

        # get the evasion before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startEvasion = stats.pEvasion
        #buy evasion
        res = self.client.post("/buypevasion/")
        assert res.status_code < 400
        # get the evasion after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endEvasion = stats.pEvasion
        # make sure evasion has increased by one
        self.assertEquals(startEvasion + 1, endEvasion)

    def test_buy_damage(self):

        # get the damage before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startDamage = stats.damage
        #buy damage
        res = self.client.post("/buydamage/")
        assert res.status_code < 400
        # get the damage after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endDamage = stats.damage
        # make sure damage has increased by one
        self.assertEquals(startDamage + 1, endDamage)

    def test_buy_accuracy(self):

        # get the accuracy before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startAccuracy = stats.accuracy
        #buy accuracy
        res = self.client.post("/buyaccuracy/")
        assert res.status_code < 400
        # get the accuracy after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endAccuracy = stats.accuracy
        # make sure accuracy has increased by one
        self.assertEquals(startAccuracy + 1, endAccuracy)

    def test_buy_attackspeed(self):

        # get the attackspeed before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startAttackSpeed = stats.attackSpeed
        #buy attackspeed
        res = self.client.post("/buyattackspeed/")
        assert res.status_code < 400
        # get the attackspeed after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endAttackSpeed = stats.attackSpeed
        # make sure attackspeed has increased by one
        self.assertEquals(startAttackSpeed + 1, endAttackSpeed)

    def test_buy_ahealth(self):

        # get the health before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startHealth = stats.aHealth
        #buy health
        res = self.client.post("/buyahealth/")
        assert res.status_code < 400
        # get the health after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endHealth = stats.aHealth
        # make sure health has increased by one
        self.assertEquals(startHealth + 1, endHealth)

    def test_buy_atoughness(self):

        # get the toughness before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startTougness = stats.aToughness
        #buy toughness
        res = self.client.post("/buyatoughness/")
        assert res.status_code < 400
        # get the toughness after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endToughness = stats.aToughness
        # make sure toughness has increased by one
        self.assertEquals(startTougness + 1, endToughness)

    def test_buy_aevasion(self):

        # get the evasion before the transaction
        stats = pStat.objects.get(player=self.pClient)
        startEvasion = stats.aEvasion
        #buy evasion
        res = self.client.post("/buyaevasion/")
        assert res.status_code < 400
        # get the evasion after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)

        endEvasion = stats.aEvasion
        # make sure evasion has increased by one
        self.assertEquals(startEvasion + 1, endEvasion)

    def test_not_enough_resources(self):

        # get the current health
        stats = pStat.objects.get(player=self.pClient)
        startHealth = stats.pHealth

        for i in range(105):
            res = self.client.post('/buyphealth/')
            assert res.status_code < 400

        # update stat block
        self.pClient = Player.objects.get(username="testUsername")
        stats = pStat.objects.get(player=self.pClient)
        endHealth = stats.pHealth

        # make sure that the health is only +100 beacuse thats how much wood they were given
        self.assertEquals(startHealth + 100, endHealth)
        # check that they have no wood
        playerRes = PlayerResource.objects.get(player=self.pClient, resource=self.res1)
        self.assertEquals(playerRes.amount, 0)
        

from django.test import TestCase, Client
from TheGame.models import Champion
# this function gets the users stats
from TheGame.processes import getUserFromName
from Login.models import Player
from Resources.processes import addResourceToUser
from Resources.models import PlayerResource, Resource
from TheGame.models import *
from TheGame.processes import *


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
        stats = Champion.objects.get(player=self.pClient)
        startHealth = stats.pHealth
        # buy health
        res = self.client.post("/buyPHealth/")
        assert res.status_code < 400
        # get the health after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = Champion.objects.get(player=self.pClient)

        endHealth = stats.pHealth
        # make sure health has increased by one
        self.assertEquals(startHealth + 1, endHealth)

    def test_buy_pAthletics(self):

        # get the toughness before the transaction
        stats = Champion.objects.get(player=self.pClient)
        startTougness = stats.pAthletics
        # buy toughness
        res = self.client.post("/buyPAthletics/")
        assert res.status_code < 400
        # get the toughness after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = Champion.objects.get(player=self.pClient)

        endToughness = stats.pAthletics
        # make sure toughness has increased by one
        self.assertEquals(startTougness + 1, endToughness)

    def test_buy_pBrain(self):

        # get the evasion before the transaction
        stats = Champion.objects.get(player=self.pClient)
        startEvasion = stats.pBrain
        # buy evasion
        res = self.client.post("/buyPBrain/")
        assert res.status_code < 400
        # get the evasion after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = Champion.objects.get(player=self.pClient)

        endEvasion = stats.pBrain
        # make sure evasion has increased by one
        self.assertEquals(startEvasion + 1, endEvasion)

    def test_buy_pControl(self):

        # get the damage before the transaction
        stats = Champion.objects.get(player=self.pClient)
        startDamage = stats.pControl
        # buy damage
        res = self.client.post("/buyPControl/")
        assert res.status_code < 400
        # get the damage after the transaction
        self.pClient = Player.objects.get(username="testUsername")
        stats = Champion.objects.get(player=self.pClient)

        endDamage = stats.pControl
        # make sure damage has increased by one
        self.assertEquals(startDamage + 1, endDamage)

    def test_not_enough_resources(self):

        # get the current health
        stats = Champion.objects.get(player=self.pClient)
        startHealth = stats.pHealth

        for i in range(105):
            res = self.client.post('/buyPHealth/')
            assert res.status_code < 400

        # update stat block
        self.pClient = Player.objects.get(username="testUsername")
        stats = Champion.objects.get(player=self.pClient)
        endHealth = stats.pHealth

        # make sure that the health is only +100 beacuse thats how much wood
        # they were given
        self.assertEquals(startHealth + 100, endHealth)
        # check that they have no wood
        playerRes = PlayerResource.objects.get(
            player=self.pClient, resource=self.res1)
        self.assertEquals(playerRes.amount, 0)


class ItemTestCase(TestCase):
    def setUp(self):

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

        self.pClient = Player.objects.get(username="testUsername")

    def testAddingItems(self):
        # test to make sure adding items works
        createNewBaseItem(
            name="ring",
            price=5,
            type="accessory",
            armourValue=15,
            vitalityBoost=50,
            specialAbilities="sleeping"
        )

        baseItem = BaseItem.objects.get(name="ring")

        self.assertEquals(baseItem.name, "ring")

        # test that we can add new specific items and give them to champions

        createNewSpecificItem(
            baseItem, 5, 2
        )

        specItem = SpecificItem.objects.get(name="ring")

        self.assertEqual(specItem.name, "ring")
        self.assertEqual(specItem.level, 5)
        self.assertEqual(specItem.glory, 2)

        # make sure that you can give this item to a champion

        mychamp = getChampion(self.pClient)

        addItemToChampion(specItem, mychamp)

        ci = ChampionItems.objects.get(pk=1)

        self.assertEqual(ci.item, specItem)
        self.assertEqual(ci.champion, mychamp)

    def testAddingWeapons(self):
        # test creating a new base weapon
        createNewBaseWeapon(
            name="sword",
            price=10,
            type="shortsword",
            damageNumber=15,
            damageInstances=3,
            range=2,
            association="c",
            ap_cost=6,
        )

        baseWeapon = BaseWeapon.objects.get(pk=1)

        self.assertEquals(baseWeapon.name, "sword")

        # now check that we can add specific weapons and give them to champion

        specWeapon = createNewSpecificItem(
            baseWeapon, 5, 2
        )

        specItem = SpecificWeapon.objects.get(name="sword")

        self.assertEqual(specItem.name, "sword")
        self.assertEqual(specItem.level, 5)
        self.assertEqual(specItem.glory, 2)

        # make sure that you can give this weapon to a champion

        mychamp = getChampion(self.pClient)

        addItemToChampion(specWeapon, mychamp)

        ci = ChampionItems.objects.get(pk=1)

        self.assertEqual(ci.item, specWeapon)
        self.assertEqual(ci.champion, mychamp)

        # make sure you cannot give a base item to a champion

        try:
            addItemToChampion(baseWeapon, mychamp)
            assert False
        except Exception:
            assert True

        # test the getter functions

        items = getChampionsItemsAndWeapons(mychamp)

        self.assertEqual(items[0], specWeapon)

        # test that we can get all the base items without getting the other ones

        baseItemsList = getAllBaseItemsAndWeapons() #should return a list of only the base weapon that was added

        # there should only be one base item because the other one is a specific item
        # this item should be the base weapon that we created
        self.assertEquals(len(baseItemsList), 1)
        self.assertEquals(baseItemsList[0], baseWeapon)

        # check that the returning functions will return the same thing
        # they should be the same because we have only added a weapon

        self.assertEqual(
            getChampionsWeapons(mychamp), getChampionsItemsAndWeapons(mychamp)
        )

        # make sure that we get an empty list if we have no items

        self.assertEqual(
            getChampionsItems(mychamp), None
        )

    def stat_pack_test(self):
        # create a new item that we can use for upgrading

        baseItem = createNewBaseItem(
            name = "shield",
            price = 10,
            type = "item",
            armourValue = 15,
            vitalityBoost = 50,
            specialAbilities = "sleeping",
        )

        specItem = createNewSpecificItem(
            baseItem = baseItem,
            startingLevel = 3,
            startingGlory = 2,
        )

        baseStatPack = createNewBaseItem(
            name = "shieldUpgradePack",
            price = 14,
            type = "statPack",
            armourValue = 10,
            vitalityBoost = 0,
            specialAbilities = "",
        )

        specStatPack = createNewSpecificItem(
            baseItem = baseStatPack,
            startingLevel = 5,
            startingGlory = 0
        )

        # apply the stat pack
        applyStatPack(specItem, specStatPack)

        # check that the item was updgraded
        self.assertEqual(specItem.armourValue, 25)

    def test_removing_items(self):
        # create an item that we can remove

        baseItem = createNewBaseItem(
            name = "shield",
            price = 10,
            type = "item",
            armourValue = 15,
            vitalityBoost = 50,
            specialAbilities = "sleeping",
        )

        specItem = createNewSpecificItem(
            baseItem = baseItem,
            startingLevel = 3,
            startingGlory = 2,
        )

        # once its removed it should also remove the spec item leaving items table empty
        self.assertEqual(baseItem.pk, 1)
        self.assertEqual(specItem.pk, 2)

        removeItemOrWeapon(baseItem)

        # there should now be no base item in the system
        self.assertEquals(
            getAllBaseItemsAndWeapons(), None
        )

        # assert that no item with pk 2 exists
        try:
            Item.objects.get(pk=2)
            assert False
        except:
            assert True
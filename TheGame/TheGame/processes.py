import json
from django.http import HttpRequest, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from Login.models import Player
from Resources.processes import *
from .models import Champion, Item
from Login.processes import getUserFromCookie
from Login.models import Player
from Resources.models import PlayerResource, Resource
from django.db.models import Q
from TheGame.models import *


def getUserFromName(request):
    """ returns a users stat block,
    you should probably use getChampion instead
    """
    user = getUserFromCookie(request)
    userStats = Champion.objects.get(player=user)
    return userStats


def getChampion(player: Player) -> Champion:
    if not (champs := Champion.objects.filter(player=player)).exists():
        return None

    return champs[0]


def spendResource(request, rNeeded, amount):
    """ spends a requested amount of a resource from a user
    """
    try:
        removeResourceFromUser(
            getUserFromCookie(request),
            rNeeded,
            amount)
        return True
    except Exception as e:
        messages.error(request, ('Not enough resources'))
        return False

def spendMultiResource(request, resources: "list[tuple(Resource,int)]"):
    user = getUserFromCookie(request)
    # check that for each resource the player has enough
    for tup in resources:
        if getPlayerResourceAmount(user, tup[0]) < tup[1]: #tup[0] = resource tup[1] = amount
            messages.error(request, ('Not enough resources'))
            return False # return false if they dont have enough
    # if execution gets here then they have enough resources so we can spend
    for tup in resources:
        if not spendResource(request, tup[0], tup[1]):
            messages.error(request, ('something has gone very wrong and you may have lost resources'))
            print("failed at res" + tup[0])
            return False
    return True



def buyPHealth(request):
    """ makes a purchase of pHealth from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.pHealth += 1
        userStats.save()

    return response


def buyPToughness(request):
    """ makes a purchase of pToughness from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")

    addResourceToUser(getUserFromCookie(request), getResourceByName('wood'), 5)
    userStats = getUserFromName(request)
    userStats.pToughness += 1
    userStats.save()

    return response


def buyPEvasion(request):
    """ makes a purchase of pEvasion from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.pEvasion += 1
        userStats.save()

    return response


def buyDamage(request):
    """ makes a purchase of damage from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.damage += 1
        userStats.save()

    return response


def buyAccuracy(request):
    """ makes a purchase of accuracy from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.accuracy += 1
        userStats.save()

    return response


def buyAttackSpeed(request):
    """ makes a purchase of attackSpeed from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.attackSpeed += 1
        userStats.save()

    return response


def buyAHealth(request):
    """ makes a purchase of aHealth from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.aHealth += 1
        userStats.save()

    return response


def buyAToughness(request):
    """ makes a purchase of aToughness from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.aToughness += 1
        userStats.save()

    return response


def buyAEvasion(request):
    """ makes a purchase of aEvasion from the user
    """
    if not request.method == "POST":
        messages.error(
            request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        userStats = getUserFromName(request)
        userStats.aEvasion += 1
        userStats.save()

    return response


def getAllBosses() -> "list[Champion]":

    if not (bosses := Champion.objects.filter(player=None)):
        return None

    bossList = []

    for b in bosses:
        bossList.append(b)

    return bossList


def addBossToSystem(request: HttpRequest):
    if not request.method == "POST":
        return HttpResponse("failed to perform operation")

    statInfo = request.POST

    itemCount = 0
    newItems = []

    try:
        if (primaryWeapon := createNewSpecificItem(getBaseItemFromName(statInfo['primaryWeapon']), 0, 0)) != None:
            itemCount += 1
            newItems.append(primaryWeapon)
            if not isinstance(primaryWeapon, SpecificWeapon):
                messages.add_message(request, messages.ERROR, 'primary weapon must be a weapon')
                raise Exception('primary weapon must be a weapon')
        primaryWeapon = None

        if (armour := createNewSpecificItem(getBaseItemFromName(statInfo['armour']), 0, 0)) != None:
            itemCount += 1
            newItems.append(armour)
            if not (isinstance(armour, SpecificItem) and armour.type == "armour"):
                messages.add_message(request, messages.ERROR, 'armour must be an armour')
                raise Exception('armour must be an armour')

        armour = None

        if (auxItem1 := createNewSpecificItem(getBaseItemFromName(statInfo['auxItem1']), 0, 0)) != None:
            itemCount += 1
            newItems.append(auxItem1)
            if not isinstance(auxItem1, SpecificItem):
                messages.add_message(request, messages.ERROR, 'aux items cannot be weapons')
                raise Exception('aux items cannot be weapons')

        auxItem1 = None

        if (auxItem2 := createNewSpecificItem(getBaseItemFromName(statInfo['auxItem2']), 0, 0)) != None:
            itemCount += 1
            newItems.append(auxItem2)
            if not isinstance(auxItem2, SpecificItem):
                messages.add_message(request, messages.ERROR, 'aux items cannot be weapons')
                raise Exception('aux items cannot be weapons')

        auxItem2 = None

        if (auxItem3 := createNewSpecificItem(getBaseItemFromName(statInfo['auxItem3']), 0, 0)) != None:
            itemCount += 1
            newItems.append(auxItem3)
            if isinstance(auxItem3, SpecificItem):
                messages.add_message(request, messages.ERROR, 'aux items cannot be weapons')
                raise Exception('aux items cannot be weapons')

        auxItem3 = None


        Champion.objects.create(
            player=None,
            name=statInfo['name'],
            pHealth=statInfo['pHealth'],
            pAthletics=statInfo['pAthletics'],
            pBrain=statInfo['pBrain'],
            pControl=statInfo['pControl'],

            primaryWeapon = primaryWeapon,
            armour = armour,
            auxItem1 = auxItem1,
            auxItem2 = auxItem2,
            auxItem3 = auxItem3,
        )
    except Exception as e:
        # if creating the champion fails delete the items so they arent left hanging
        for i in range(itemCount):
            print(i)
            print(newItems[i].name)
            removeItemOrWeapon(newItems[i])

    return HttpResponseRedirect('addBosses')


def buyPHealth(request):
    """ makes a purchase of aEvasion from the user
    """
    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pHealth += 1
        userChamp.save()
    else:
        messages.error(request, ('xH'))

    return response


def buyPAthletics(request):
    """ makes a purchase of athlectics from the user
    """
    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pAthletics += 1
        userChamp.save()
    else:
        messages.error(request, ('xA'))

    return response


def buyPBrain(request):
    """ makes a purchase of brains from the user
    """
    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pBrain += 1
        userChamp.save()
    else:
        messages.error(request, ('xB'))

    return response


def buyPControl(request):
    """ makes a purchase of control from the user
    """
    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request, getResourceByName('wood'), 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pControl += 1
        userChamp.save()
    else:
        messages.error(request, ('xC'))

    return response


def buyItem(request):
    """ makes a purchase of an item for the user
    """

    data = request.body.decode('utf-8')  # decode the body to a string
    requestJson = json.loads(data)  # load json from string data
    itemPK = requestJson['itemPk']

    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterShop")

    item = getItemFromPK(itemPK)

    resList = [(item.priceRes1, item.price1)]
    if item.priceRes2:
        resList.append((item.priceRes2, item.price2))
    if item.priceRes3:
        resList.append((item.priceRes3, item.price3))

    if spendMultiResource(request, resList):
        print("spent")
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        addItemToChampion(createNewSpecificItem(item, 0, 0), userChamp)

    return response


def equipItem(request):
    """ makes an equip of an item for the user
    """

    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    response = redirect("/characterInventory")
    item = getItemFromPK(request.POST.get('itemPK'))
    user = getUserFromCookie(request)
    userChamp = getChampion(user)
    # To be contuinued....
    # replace the foriegn keys in the champions places with the item that was bought
    # this will have to have logic for when all slots are full

    if item.type == "statPack":
        return response

    if isEquiped(userChamp, item):
        return response
    elif isinstance(item, SpecificWeapon):
        userChamp.primaryWeapon = item
    elif isinstance(item, SpecificItem) and item.type == "armour":
        userChamp.armour = item
    elif not userChamp.auxItem1:
        userChamp.auxItem1 = item
    elif not userChamp.auxItem2:
        userChamp.auxItem2 = item
    elif not userChamp.auxItem3:
        userChamp.auxItem3 = item

    userChamp.save()
        

    return response

def unequipItem(request):
    """ makes an unequip of an item for the user
    """

    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    response = redirect("/characterInventory")
    item = getItemFromPK(request.POST.get('itemPK'))
    user = getUserFromCookie(request)
    userChamp = getChampion(user)

    if isinstance(item, SpecificWeapon):
        userChamp.primaryWeapon = None
    elif isinstance(item, SpecificItem) and item.type == "armour":
        userChamp.armour = None
    elif userChamp.auxItem1 == item:
        userChamp.auxItem1 = None
    elif userChamp.auxItem2 == item:
        userChamp.auxItem2 = None
    elif userChamp.auxItem3 == item:
        userChamp.auxItem3 = None

    userChamp.save()
        

    return response


def sellItem(request):
    """ makes a sell of an item for the user
    """

    data = request.body.decode('utf-8')  # decode the body to a string
    requestJson = json.loads(data)  # load json from string data
    itemPK = requestJson['itemPK']

    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    item = getItemFromPK(itemPK)
    user = getUserFromCookie(request)
    userChamp = getChampion(user)

    addResourceToUser(user, item.priceRes1, item.price1)
    if item.priceRes2:
        addResourceToUser(user, item.priceRes2, item.price2)
    if item.priceRes3:
        addResourceToUser(user, item.priceRes3, item.price3)
        
    removeItemFromChampion(userChamp, item)
    removeItemOrWeapon(item)

    return HttpResponse(status=200)


def upgradeStatOnItem(request):
    """ makes a sell of an item for the user
    """

    data = request.body.decode('utf-8')  # decode the body to a string
    requestJson = json.loads(data)  # load json from string data
    itemPK = requestJson['itemPK']
    packPK = requestJson['packPK']
    pack = getItemFromPK(packPK)
    print(pack)

    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    # response = redirect("/itemUpgrade") # need to pass parameters so that
    # the item upgrade page knows what itemPK is
    item = getItemFromPK(itemPK)
    user = getUserFromCookie(request)
    userChamp = getChampion(user)
    # To be contuinued....

    # if the item is a weapon then get the first weapon statpack from the use
    if not applyStatPack(item, pack):
        return HttpResponse("no stat packs found", status=202)

    removeItemFromChampion(userChamp, pack)
    removeItemOrWeapon(pack)


    return HttpResponse(status=200)

#
#   THESE ARE THE FUNCTIONS THAT WILL DEAL WITH CREATING AND REMOVING ITEMS
#


def getItemFromPK(pk: int) -> Item:

    try:
        item = Item.objects.get(pk=pk)
        return item
    except:
        return None


def createNewBaseItem(name: str, type: str,
                      armourValue: int, vitalityBoost: int, shieldValue:int,
                      specialAbilities: str,
                      priceRes1: Resource, price1: int,
                      priceRes2: Resource = None, price2: int = None,
                      priceRes3: Resource = None, price3: int = None) -> BaseItem:
    """ this function will create a new BaseItem in the database,
    Args:
        name(Str): name of the item
        price(int): price of the item
        type(str): the type of the item
        armourValue(int): armour value of the item
        vitalityBoost(int): vitality boost of the item
        specialAbilities(str): string representing the special abilities of the item

    returns:
        instance of the item that was created
        if item already exists then the existing item is returned
    """

    # create the base item in the database

    query = ~Q(instance_of=SpecificItem) & Q(name=name)

    if (baseItem := BaseItem.objects.filter(query)).exists():
        return baseItem[0]

    baseItem = BaseItem.objects.create(
        name=name,
        priceRes1=priceRes1,
        priceRes2=priceRes2,
        priceRes3=priceRes3,
        price1=price1,
        price2=price2,
        price3=price3,
        type=type,
        armourValue=armourValue,
        vitalityBoost=vitalityBoost,
        shieldValue=shieldValue,
        specialAbilities=specialAbilities,
    )

    return baseItem


def createNewSpecificItem(
        baseItem: BaseItem, startingLevel: int, startingGlory: int) -> SpecificItem:
    """ function to create a new specific item from a base item
    Args:
        baseItem(BaseItem): the item base to use
        startingLevel(int): the level that this specific item will be created at
        startingGlory(int): the glory level that this specific item will be created at

    returns:
        the Specific item that was created
    """

    # create the specific item based on the base item

    if isinstance(baseItem, BaseItem):
        si = SpecificItem.objects.create(
            name=baseItem.name,
            type=baseItem.type,

            priceRes1=baseItem.priceRes1,
            priceRes2=baseItem.priceRes2,
            priceRes3=baseItem.priceRes3,
            price1=baseItem.price1,
            price2=baseItem.price2,
            price3=baseItem.price3,

            armourValue=baseItem.armourValue,
            vitalityBoost=baseItem.vitalityBoost,
            shieldValue=baseItem.shieldValue,
            specialAbilities=baseItem.specialAbilities,

            level=startingLevel,
            glory=startingGlory,
        )

        return si

    elif isinstance(baseItem, BaseWeapon):
        sw = SpecificWeapon.objects.create(
            name=baseItem.name,
            type=baseItem.type,

            priceRes1=baseItem.priceRes1,
            priceRes2=baseItem.priceRes2,
            priceRes3=baseItem.priceRes3,
            price1=baseItem.price1,
            price2=baseItem.price2,
            price3=baseItem.price3,

            damageNumber=baseItem.damageNumber,
            damageInstances=baseItem.damageInstances,
            range=baseItem.range,
            associated=baseItem.associated,
            ap_cost=baseItem.ap_cost,

            level=startingLevel,
            glory=startingGlory,
        )

        return sw


def createNewBaseWeapon(name: str, type: str,
                        damageNumber: int, damageInstances: int, range: int, association: chr, ap_cost: int,
                        priceRes1: Resource, price1: int,
                        priceRes2: Resource = None, price2: int = None,
                        priceRes3: Resource = None, price3: int = None) -> BaseWeapon:
    """ this function will create a new BaseWeapon in the database,
    Args:
        name(Str): name of the item
        price(int): price of the item
        type(str): the type of the item
        damageNumber(int): the amount of damage the weapon deals per instance
        damageInstances(int): the number of damage instances the weapon has per attack
        range(int): the range that the weapon can damage from
        association(chr): the weapons association should be in ['A','B','C']
    returns:
        instance of the weapon that was created
        if weapon already exists then the existing weapon is returned
    """

    # create the base weapon instance

    query = ~Q(instance_of=SpecificWeapon) & Q(name=name)

    if (bw := BaseWeapon.objects.filter(query)).exists():
        return bw[0]

    bw = BaseWeapon.objects.create(
        name=name,
        type=type,
        priceRes1=priceRes1,
        priceRes2=priceRes2,
        priceRes3=priceRes3,
        price1=price1,
        price2=price2,
        price3=price3,

        damageInstances=damageInstances,
        damageNumber=damageNumber,
        range=range,
        associated=association,
        ap_cost=ap_cost
    )

    return bw


def getBaseItemFromName(name: str) -> Item:
    """ function that will return the base item model from its name
    this can be used to get a weapon or item

    Args:
        name(str): the name of the item that you want

    returns:
        Item: this will be an instance of BaseItem or BaseWeapon depending on the item
        returns None if the item doesnt exist
    """

    # get the item
    query = ~Q(instance_of=SpecificItem) & ~Q(instance_of=SpecificWeapon) & Q(name=name)
    try:
        item = Item.objects.get(query)
        return item
    except:
        return None

    return None


def addItemToChampion(item: Item, champion: Champion):
    if not (isinstance(item, SpecificItem)
            or isinstance(item, SpecificWeapon)):
        raise Exception("item must be a specific item or weapon")

    if ChampionItems.objects.filter(champion=champion, item=item).exists():
        return

    ChampionItems.objects.create(
        champion=champion,
        item=item,
    )


def getChampionsItemsAndWeapons(champion: Champion) -> "list[Item]":
    """ function that returns a list of all the items and weapons in a champions possession
    Args:
        champion(Champion): the champion that you want to get the items for

    returns:
        a list of all the items and weapons that that champion has
    """

    if not (champItems := ChampionItems.objects.filter(
            champion=champion)).exists():
        return None

    itemList = []

    for ci in champItems:
        itemList.append(ci.item)

    return itemList


def getChampionsItems(champion: Champion) -> "list[Item]":
    """ function that returns a list of all the items in a champions possession
    Args:
        champion(Champion): the champion that you want to get the items for

    returns:
        a list of all the items that that champion has
    """

    if not (champItems := ChampionItems.objects.filter(
            champion=champion)).exists():
        return None

    itemList = []

    for ci in champItems:
        if isinstance(ci.item, SpecificItem):
            itemList.append(ci.item)

    if itemList == []:
        return None

    return itemList


def getChampionsWeapons(champion: Champion) -> "list[Item]":
    """ function that returns a list of all the weapons in a champions possession
    Args:
        champion(Champion): the champion that you want to get the items for

    returns:
        a list of all the weapons that that champion has
    """

    if not (champItems := ChampionItems.objects.filter(
            champion=champion)).exists():
        return None

    itemList = []

    for ci in champItems:
        if isinstance(ci.item, BaseWeapon):
            itemList.append(ci.item)

    if itemList == []:
        return None

    return itemList


def removeItemOrWeapon(item: Item):
    """ function that will remove all the item in the database, note that this will also remove
    any specific instances of that item
    """
    if isinstance(item, SpecificItem) or isinstance(item, SpecificWeapon):
        item.delete()
        return

    instances = SpecificItem.objects.filter(name=item.name)

    for i in instances:
        i.delete()

    item.delete()


def getAllBaseItemsAndWeapons() -> "list[Item]":
    """ function that returns a list of all base items and weapons

    returns:
        list of all base items and weapons in the system
    """

    query = ~Q(instance_of=SpecificItem) & ~Q(instance_of=SpecificWeapon)

    if (items := Item.objects.filter(query)) is None:
        return None

    itemList = []
    for i in items:
        itemList.append(i)

    if itemList == []:
        return None

    return itemList


def getAllBaseItems() -> "list[Item]":
    """ function that returns a list of all base items

    returns:
        list of all base items in the system
    """

    query = ~Q(instance_of=SpecificItem)

    if (items := BaseItem.objects.filter(query)) is None:
        return None

    itemList = []
    for i in items:
        itemList.append(i)

    return itemList


def getAllBaseWeapons() -> "list[Item]":
    """ function that returns a list of all base weapons

    returns:
        list of all base weapons in the system
    """

    query = ~Q(instance_of=SpecificWeapon)

    if (items := BaseWeapon.objects.filter(query)) is None:
        return None

    itemList = []
    for i in items:
        itemList.append(i)

    return itemList


def createNewBaseItemFromHTMLRequest(request):

    data = request.POST

    response = HttpResponseRedirect('addItems')

    try:
        priceRes1 = getResourceByName(data['priceRes1'])
        price1 = int(data['price1'])
    except:
        return HttpResponseRedirect(status=501)
    try:
        priceRes2 = getResourceByName(data['priceRes2'])
        price2 = int(data['price2'])
    except:
        priceRes2 = None
        price2 = None
    try:
        priceRes3 = getResourceByName(data['priceRes3'])
        price3 = int(data['price3'])
    except:
        priceRes3 = None
        price3 = None


    try:
        if data['itemType'] == "item":
            createNewBaseItem(
                name=data['name'],
                type=data['type'],
                armourValue=data['armourValue'],
                vitalityBoost=data['vitalityBoost'],
                shieldValue=data['shieldValue'],
                specialAbilities=data['specialAbilities'],
                priceRes1=getResourceByName(data['priceRes1']),
                price1=data['price1'],
                priceRes2=priceRes2,
                price2=price2,
                priceRes3=priceRes3,
                price3=price3,
            )

        elif data['itemType']:
            createNewBaseWeapon(
                name=data['name'],
                type=data['type'],
                damageNumber=data['damageNumber'],
                damageInstances=data['damageInstances'],
                range=data['range'],
                association=data['associated'],
                ap_cost=data['ap_cost'],

                priceRes1=getResourceByName(data['priceRes1']   ),
                price1=data['price1'],
                priceRes2=priceRes2,
                price2=price2,
                priceRes3=priceRes3,
                price3=price3,
            )

        return response

    except Exception as e:
        messages.add_message(request, messages.ERROR, e)
        return response

def getChampionsItemStatPacks(champion : Champion) -> "list[SpecificItem]":
    """ function that will return a list of all the users item stat packs
    """

    query = Q(champion=champion) & Q(item__type="statPack")

    #query the table for the stat packs

    if not (statpacks := ChampionItems.objects.filter(query)).exists():
        return None

    packList = []

    for pack in statpacks:
        if isinstance(pack.item, SpecificItem):
            packList.append(pack.item)

    return packList

def getChampionsWeaponStatPacks(champion : Champion) -> "list[SpecificItem]":
    """ function that will return a list of all the users item stat packs
    """

    query = Q(champion=champion) & Q(item__type="statPack")

    #query the table for the stat packs

    if not (statpacks := ChampionItems.objects.filter(query)).exists():
        return None

    packList = []

    for pack in statpacks:
        if isinstance(pack.item, SpecificWeapon):
            packList.append(pack.item)

    return packList

def getAllChampionUnequipedItems(champion: Champion):

    if not (champItems := ChampionItems.objects.filter(
        champion=champion)).exists():
        return None

    itemList = []

    for ci in champItems:
        if not isEquiped(champion, ci.item):
            itemList.append(ci.item)

    return itemList

def isEquiped(champion: Champion, item: Item) -> bool:
    if champion.primaryWeapon == item:
        return True
    elif champion.secondaryWeapon == item:
        return True
    elif champion.armour == item:
        return True
    elif champion.auxItem1 == item:
        return True       
    elif champion.auxItem2 == item:
        return True       
    elif champion.auxItem3 == item:
        return True
    return False
    

def removeItemFromChampion(champion: Champion, item: Item):
    """function that will remove an item from a champion
    """

    # make sure the item isnt equipt

    uneqipFromChampion(champion, item)

    query = Q(champion=champion) & Q(item=item)
    
    try:
        ChampionItems.objects.get(query).delete()
        return True
    except:
        return False

def uneqipFromChampion(champion: Champion, item: Item):

    if champion.primaryWeapon == item:
        champion.primaryWeapon = None
    elif champion.secondaryWeapon == item:
        champion.secondaryWeapon = None
    elif champion.armour == item:
        champion.armour = None
    elif champion.auxItem1 == item:
        champion.auxItem1 = None        
    elif champion.auxItem2 == item:
        champion.auxItem2 = None        
    elif champion.auxItem3 == item:
        champion.auxItem3 = None        

    champion.save()

def getItemFromPK(pk: int) -> Item:
    
    try:
        item = Item.objects.get(pk=pk)
        return item
    except:
        return None

def applyStatPack(item: Item, statPack: Item):

    if item == statPack:
        return False

    if isinstance(item, SpecificItem):
        if not (isinstance(statPack, SpecificItem) and statPack.type == "statPack"):
            raise Exception("item can only be upgraded with a stat pack of the same type")
        
        item.armourValue += statPack.armourValue
        item.vitalityBoost += statPack.vitalityBoost
        item.shieldValue += statPack.shieldValue
        item.level += statPack.level
        item.save()
        return True

    elif isinstance(item, SpecificWeapon):
        if not (isinstance(statPack, SpecificWeapon) and statPack.type == "statPack"):
            raise Exception("item can only be upgraded with a stat pack of the same type")
        
        item.damageNumber += statPack.damageNumber
        item.damageInstances += statPack.damageInstances
        item.range += statPack.range
        item.level += statPack.level
        item.save()
        return True
        
    elif isinstance(statPack, Item):
        raise Exception("must use a stat pack of correct type of the statpack to apply to item")
    
    raise Exception("failed to apply statPack to item")


def getShields(champion : Champion):
    i = getItemFromPK(champion.armour)
    shield = 0
    if i:
        shield = shield + i.shieldValue
    i = getItemFromPK(champion.auxItem1)
    if i:
        shield = shield + i.shieldValue
    i = getItemFromPK(champion.auxItem2)
    if i:
        shield = shield + i.shieldValue
    i = getItemFromPK(champion.auxItem3)
    if i:
        shield = shield + i.shieldValue
    return shield

def getArmour(champion : Champion):
    i = getItemFromPK(champion.armour)
    armr = 0
    if i:
        armr = armr + i.armourValue
    i = getItemFromPK(champion.auxItem1)
    if i:
        armr = armr + i.armourValue
    i = getItemFromPK(champion.auxItem2)
    if i:
        armr = armr + i.armourValue
    i = getItemFromPK(champion.auxItem3)
    if i:
        armr = armr + i.armourValue
    return armr

def getVitBoost(champion: Champion):
    i = getItemFromPK(champion.armour)
    vit = 0
    if i:
        vit = vit + i.vitalityBoost
    i = getItemFromPK(champion.auxItem1)
    if i:
        vit = vit + i.vitalityBoost
    i = getItemFromPK(champion.auxItem2)
    if i:
        vit = vit + i.vitalityBoost
    i = getItemFromPK(champion.auxItem3)
    if i:
        vit = vit + i.vitalityBoost
    return vit

def getGlory(champion: Champion):
    i = getItemFromPK(champion.armour)
    glr = 0
    if i:
        glr = glr + i.vitalityBoost
    i = getItemFromPK(champion.auxItem1)
    if i:
        glr = glr + i.vitalityBoost
    i = getItemFromPK(champion.auxItem2)
    if i:
        glr = glr + i.vitalityBoost
    i = getItemFromPK(champion.auxItem3)
    if i:
        glr = glr + i.vitalityBoost
    i = getItemFromPK(champion.primaryWeapon)
    if i:
        glr = glr + i.vitalityBoost
    return glr
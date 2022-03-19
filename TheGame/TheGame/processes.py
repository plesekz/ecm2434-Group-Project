from logging import exception
from operator import truediv
from django.http import HttpRequest, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from Login.models import Player
from Resources.processes import removeResourceFromUser, addResourceToUser, getResourceByName
from .models import Champion
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

def getChampion(player : Player) -> Champion:
    if not (champs := Champion.objects.filter(player=player)).exists():
        return None

    return champs[0]


def spendResource(request, rNeeded, amount):
    """ spends a requested amount of a resource from a user
    """
    try:
        removeResourceFromUser(getUserFromCookie(request), getResourceByName(rNeeded), amount)
        return True
    except Exception as e:
        messages.error(request, ('Not enough resources'))
        return False


def getAllBosses() -> "list[Champion]":

    if not (bosses := Champion.objects.filter(player=None)):
        return None

    bossList = []

    for b in bosses:
        bossList.append(b)

    return bossList

def addBossToSystem(request : HttpRequest):
    if not request.method == "POST":
        return HttpResponse("failed to perform operation")

    statInfo = request.POST

    Champion.objects.create(
        player=None,
        name = statInfo['name'],
        pHealth =  statInfo['pHealth'],
        pAthletics = statInfo['pAthletics'],
        pBrain = statInfo['pBrain'],
        pControl = statInfo['pControl'],
    )

    return HttpResponseRedirect('addBosses')


def buyPHealth(request):
    """ makes a purchase of aEvasion from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pHealth += 1
        userChamp.save()

    return response


def buyPAthletics(request):
    """ makes a purchase of athlectics from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pAthletics += 1
        userChamp.save()

    return response

def buyPBrain(request):
    """ makes a purchase of brains from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pBrain += 1
        userChamp.save()

    return response

def buyPControl(request):
    """ makes a purchase of control from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        user = getUserFromCookie(request)
        userChamp = getChampion(user)
        userChamp.pControl += 1
        userChamp.save()

    return response

#
#   THESE ARE THE FUNCTIONS THAT WILL DEAL WITH CREATING AND REMOVING ITEMS
#

def createNewBaseItem(name : str, price : int, type : str,
    armourValue : int, vitalityBoost : int, specialAbilities : str) -> BaseItem:

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

    if baseItem := BaseItem.objects.filter(name=name).exists():
        return baseItem[0]


    baseItem = BaseItem.objects.create(
        name = name,
        price = price,
        type = type,
        armourValue = armourValue,
        vitalityBoost = vitalityBoost,
        specialAbilities = specialAbilities,
    )

    return baseItem

def createNewSpecificItem(baseItem : BaseItem, startingLevel : int, startingGlory : int) -> SpecificItem:
    """ function to create a new specific item from a base item
    Args:
        baseItem(BaseItem): the item base to use
        startingLevel(int): the level that this specific item will be created at
        startingGlory(int): the glory level that this specific item will be created at

    returns:
        the Specific item that was created
    """

    # create the specific item based on the base item
    si = SpecificItem.objects.create(
        name = baseItem.name,
        price = baseItem.price,
        type = baseItem.type,

        armourValue = baseItem.armourValue,
        vitalityBoost = baseItem.vitalityBoost,
        specialAbilities = baseItem.specialAbilities,

        level = startingLevel,
        glory = startingGlory,
    )

    return si


def createNewBaseWeapon(name : str, price : int, type : str,
    damageNumber : int, damageInstances : int, range : int, association : chr, ap_cost : int) -> BaseWeapon:

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

    if bw := BaseWeapon.objects.filter(name=name).exists():
        return bw[0]

    bw = BaseWeapon.objects.create(
        name = name,
        price = price,
        type = type,

        damageInstances = damageInstances,
        damageNumber = damageNumber,
        range = range,
        associated = association,
        ap_cost = ap_cost
    )

    return bw

def createNewSpecificWeapon(baseWeapon : BaseItem, startingLevel : int, startingGlory : int) -> SpecificWeapon:
    """ function to create a new specific weapon from a base weapon
    Args:
        baseWeapon(BaseWeapon): the weapon base to use
        startingLevel(int): the level that this specific weapon will be created at
        startingGlory(int): the glory level that this specific weapon will be created at

    returns:
        the Specific weapon that was created
    """

    # create the specific item based on the base item
    sw = SpecificWeapon.objects.create(
        name = baseWeapon.name,
        price = baseWeapon.price,
        type = baseWeapon.type,

        damageNumber = baseWeapon.damageNumber,
        damageInstances = baseWeapon.damageInstances,
        range = baseWeapon.range,
        associated = baseWeapon.associated,
        ap_cost = baseWeapon.ap_cost,

        level = startingLevel,
        glory = startingGlory,
    )

    return sw

def getBaseItemFromName(name : str) -> Item:
    """ function that will return the base item model from its name
    this can be used to get a weapon or item

    Args:
        name(str): the name of the item that you want

    returns:
        Item: this will be an instance of BaseItem or BaseWeapon depending on the item
        returns None if the item doesnt exist
    """

    # get the item
    if item := Item.get(instance_of=BaseItem, name=name):
        return item

    return None

def addItemToChampion(item : Item, champion : Champion):
    if not (isinstance(item, SpecificItem) or isinstance(item, SpecificWeapon)):
        raise Exception("item must be a specific item or weapon")

    if ChampionItems.objects.filter(champion=champion, item=item).exists():
        return

    ChampionItems.objects.create(
        champion=champion,
        item=item,
    )

def getChampionsItemsAndWeapons(champion : Champion) -> "list[Item]":
    """ function that returns a list of all the items and weapons in a champions possession
    Args:
        champion(Champion): the champion that you want to get the items for

    returns:
        a list of all the items and weapons that that champion has
    """

    if not (champItems := ChampionItems.objects.filter(champion=champion).exists()):
        return None

    itemList = []

    for ci in champItems:
        itemList.append(ci.item)

    return itemList

def getChampionsItems(champion : Champion) -> "list[Item]":
    """ function that returns a list of all the items in a champions possession
    Args:
        champion(Champion): the champion that you want to get the items for

    returns:
        a list of all the items that that champion has
    """

    if not (champItems := ChampionItems.objects.filter(champion=champion).exists()):
        return None

    itemList = []

    for ci in champItems:
        if isinstance(ci, SpecificItem):
            itemList.append(ci.item)

    return itemList

def getChampionsWeapons(champion : Champion) -> "list[Item]":
    """ function that returns a list of all the weapons in a champions possession
    Args:
        champion(Champion): the champion that you want to get the items for

    returns:
        a list of all the weapons that that champion has
    """

    if not (champItems := ChampionItems.objects.filter(champion=champion).exists()):
        return None

    itemList = []

    for ci in champItems:
        if isinstance(ci, SpecificWeapon):
            itemList.append(ci.item)

    return itemList

def removeBaseItemOrWeapon(item : Item):
    """ function that will remove all the item in the database, note that this will also remove
    any specific instances of that item
    """

    if not (isinstance(item, BaseItem) or isinstance(item, BaseWeapon)):
        raise Exception("item was not a base item or weapon")

    instances = SpecificItem.objects.filter(name=item.name)

    for i in instances:
        i.remove()

    item.remove()

def getAllBaseItemsAndWeapons() -> "list[Item]":
    """ function that returns a list of all base items and weapons

    returns:
        list of all base items and weapons in the system
    """

    query = Q(instance_of=BaseItem) | Q(instance_of=BaseWeapon)

    if (items := Item.objects.filter(query)) == None:
        return None

    itemList = []
    for i in items:
        itemList.append(i)

    return itemList

def getAllBaseItems() -> "list[Item]":
    """ function that returns a list of all base items

    returns:
        list of all base items in the system
    """

    query = Q(instance_of=BaseItem)

    if (items := Item.objects.filter(query)) == None:
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

    query = Q(instance_of=BaseWeapon)

    if (items := Item.objects.filter(query)) == None:
        return None

    itemList = []
    for i in items:
        itemList.append(i)

    return itemList

def createNewBaseItemFromHTMLRequest(request):
    
    data = request.POST

    if data['itemType'] == "item":
        createNewBaseItem(
            name = data['name'],
            price = data['price'],
            type = data['type'],
            armourValue= data['armourValue'],
            vitalityBoost= data['vitalityBoost'],
            specialAbilities= data['specialAbilities']
        )

    elif data['itemType']:
        createNewBaseWeapon(
            name = data['name'],
            price = data['price'],
            type = data['type'],
            damageNumber= data['damageNumber'],
            damageInstances= data['damageInstances'],
            range= data['range'],
            association = data['associated'],
            ap_cost= data['ap_cost']
        )

    return HttpResponseRedirect('addItems')
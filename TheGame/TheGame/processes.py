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

def buyPHealth(request):
    """ makes a purchase of pHealth from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.pHealth += 1
        userStats.save()
    
    return response

def buyPToughness(request):
    """ makes a purchase of pToughness from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
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
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.pEvasion += 1
        userStats.save()    

    return response

def buyDamage(request):
    """ makes a purchase of damage from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.damage += 1
        userStats.save()
    
    return response

def buyAccuracy(request):
    """ makes a purchase of accuracy from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.accuracy += 1
        userStats.save()    

    return response

def buyAttackSpeed(request):
    """ makes a purchase of attackSpeed from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.attackSpeed += 1
        userStats.save()    

    return response

def buyAHealth(request):
    """ makes a purchase of aHealth from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.aHealth += 1
        userStats.save()
    
    return response

def buyAToughness(request):
    """ makes a purchase of aToughness from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
        userStats = getUserFromName(request)
        userStats.aToughness += 1
        userStats.save()    

    return response

def buyAEvasion(request):
    """ makes a purchase of aEvasion from the user
    """
    if not request.method == "POST":
        messages.error(request, ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"
    response = redirect("characterMenu")
    if spendResource(request,  'wood', 1):
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

def addBossToSystem(request : HttpRequest):
    if not request.method == "POST":
        return HttpResponse("failed to perform operation")

    statInfo = request.POST;

    Champion.objects.create(
        player=None,
        name = statInfo['name'],
        pHealth =  statInfo['pHealth'],
        pToughness = statInfo['pToughness'],
        pEvasion = statInfo['pEvasion'],
        damage = statInfo['damage'],
        accuracy = statInfo['accuracy'],
        attackSpeed = statInfo['attackSpeed'],
        aHealth = statInfo['aHealth'],
        aToughness = statInfo['aToughness'],
        aEvasion = statInfo['aEvasion'],
    )

    return HttpResponseRedirect('addBosses')


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

    if baseItem := BaseItem.objects.get(name=name):
        return baseItem


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
        specialAbilites = baseItem.specialAbilities,

        level = startingLevel,
        glory = startingGlory,
    )

    return si


def createNewBaseWeapon(name : str, price : int, type : str,
    damageNumber : int, damageInstances : int, range : int, association : chr) -> BaseWeapon:

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

    if bw := BaseWeapon.objects.get(name=name):
        return bw

    bw = BaseWeapon.objects.create(
        name = name,
        price = price,
        type = type,

        damageInstances = damageInstances,
        damageNumber = damageNumber,
        range = range,
        associated = association
    )

    return bw

def createNewSpecificItem(baseWeapon : BaseItem, startingLevel : int, startingGlory : int) -> SpecificWeapon:
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
        damageInstance = baseWeapon.damageInstances,
        range = baseWeapon.range,
        associated = baseWeapon.associated,

        level = startingLevel,
        glory = startingGlory,
    )

    return sw

def addItemToChampion(item : Item, champion : Champion):
    if not (isinstance(item, SpecificItem) or isinstance(item, SpecificWeapon)):
        raise Exception("item must be a specific item or weapon")

    if ChampionItems.objects.get(champion=champion, item=item):
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
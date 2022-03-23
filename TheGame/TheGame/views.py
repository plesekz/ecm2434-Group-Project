from importlib import resources
import json
from django.template import loader
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from Login.processes import getUserFromCookie
from QRC.models import QRResource, QRC
from Login.processes import is_game_master
from TheGame.processes import getAllChampionUnequipedItems, getUserFromName, getChampionFromID, createNewSpecificItem, createNewBaseWeapon
from TheGame.models import SpecificItem
from TheGame.processes import getAllBaseItems, getAllBosses, getChampionsItemStatPacks, getChampionsWeaponStatPacks, getUserFromName, getChampion, getChampionsItemsAndWeapons, addItemToChampion, getAllBaseItemsAndWeapons, getItemFromPK
from Resources.processes import getAllUserResources, getAllResources
from Resources.models import PlayerResource, Resource
from TheGame.combat_root import battle


def homePageView(request: HttpRequest) -> HttpResponse:
    """ creates response for the Home page
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    try:
        user = getUserFromCookie(request)
        champion = getChampion(user)
        resources = getAllUserResources(user)
    except Exception as e:
        print(e)
        return redirect('/login')

    template = loader.get_template('TheGame/HomePage.html')
    context = {
        "user": user,
        "champion": champion,
        "resources": resources
    }

    output = template.render(context, request)

    return HttpResponse(output)


def characterMenu(request: HttpRequest) -> HttpResponse:
    """ creates response for the character menu
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return redirect('createChampion')

    template = loader.get_template('TheGame/CharacterMenu.html')

    resources = getAllUserResources(user)

    context = {
        "username": user.username,
        "champion": champion,
        # # item stats would replace this when item database is created
        # "damage": champion.damage,
        # "accuracy": champion.accuracy,
        # "attackSpeed": champion.attackSpeed,
        # # armour stats would replace this when armour database is created
        # "aHealth": champion.aHealth,
        # "aToughness": champion.aToughness,
        # "aEvasion": champion.aEvasion,
        "resources": resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)

def map(request: HttpRequest) -> HttpResponse:
    """ creates response for the map
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return redirect('createChampion')

    codes = []
    for QRCode in QRC.objects.all():
        codes.append(
            {
                'name': QRCode.QRID,
                'lat': QRCode.latitude,
                'lon': QRCode.longitude,
                'resources': QRResource.objects.filter(QRID=QRCode),
                'imagePath': QRCode.image,
                'staticPath': "QRC/qrImages/"
            }
        )

    template = loader.get_template('TheGame/map.html')

    resources = getAllUserResources(user)

    context = {
        "username": user.username,
        "champion": champion,
        "resources": resources,
        "active_QR_codes_list": codes,
    }

    output = template.render(context, request)

    return HttpResponse(output)


def characterInventory(request: HttpRequest) -> HttpResponse:
    """ creates response for the character menu
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return redirect('createChampion')

    template = loader.get_template('TheGame/CharacterInventory.html')

    items = getAllChampionUnequipedItems(champion)

    context = {
        "username": user.username,
        "champion": champion,
        "items": items,
    }

    output = template.render(context, request)

    return HttpResponse(output)


def characterShop(request: HttpRequest) -> HttpResponse:
    """ creates response for the character menu
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return redirect('createChampion')

    template = loader.get_template('TheGame/CharacterShop.html')

    allItems = getAllBaseItemsAndWeapons()
    resources = getAllUserResources(user)

    context = {
        "username": user.username,
        "champion": champion,
        "allItems": allItems,
        "resources": resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)

def itemUpgrade(request: HttpRequest) -> HttpResponse:
    """ creates response for the item Upgrade
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return redirect('createChampion')

    template = loader.get_template('TheGame/ItemUpgrade.html')
    item = getItemFromPK(request.POST.get('itemPK'))
    resources = getAllUserResources(user)

    if isinstance(item, SpecificItem):
        statPacks = getChampionsItemStatPacks(champion)
    else:
        statPacks = getChampionsWeaponStatPacks(champion)

    context = {
        "username": user.username,
        "champion": champion,
        "item": item,
        "resources": resources,
        "statPacks": statPacks
    }

    output = template.render(context, request)

    return HttpResponse(output)


def battleSelectView(request: HttpRequest) -> HttpResponse:
    """ create response for the battle selection page
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)

    if not (champ := getChampion(user)):
        return redirect('createChampion')

    resources = getAllUserResources(user)

    bosses = getAllBosses()

    template = loader.get_template('TheGame/battleSelect.html')
    context = {
        "user": user,
        "champion": champ,
        "resources": resources,
        "bosses": bosses,
        "resources": resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)


def createChampionView(request):
    return HttpResponse("this is the champion create page")


def addNewBossView(request):
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    if not is_game_master(request.COOKIES.get('TheGameSessionID')):
        return redirect('/')

    template = loader.get_template('TheGame/newBoss.html')

    bosses = getAllBosses()
    items = getAllBaseItemsAndWeapons()

    context = {
        "bosses": bosses,
        "items": items,
    }

    output = template.render(context, request)

    return HttpResponse(output)


def addNewBaseItemView(request):
    """ returns html for the page for adding new items
    """

    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    if not is_game_master(request.COOKIES.get('TheGameSessionID')):
        return redirect('/')

    template = loader.get_template('TheGame/addNewItemTemplate.html')

    items = getAllBaseItemsAndWeapons()
    resources = getAllResources()

    context = {
        "items": items,
        "resources" : resources
    }

    output = template.render(context, request)

    return HttpResponse(output)

def battleChampion(request):
    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    bossPK = request.POST.get('bossPK')

    att = getUserFromName(request)
    deff = getChampionFromID(bossPK)

    configData = json.load(open("config.json"))
    damage = configData["unarmedWeapon"]['damage']
    damageInstances = configData["unarmedWeapon"]['damageInstances']
    range = configData["unarmedWeapon"]['range']
    association = configData["unarmedWeapon"]['association']
    apCost = configData["unarmedWeapon"]['apCost']

    if att.primaryWeapon is None:
        att.primaryWeapon = createNewSpecificItem(createNewBaseWeapon("Unarmed", "weapon", damage, damageInstances, range, association, apCost, Resource.objects.get(name="Books"), 1), 0, 0)
    
    if deff.primaryWeapon is None:
        deff.primaryWeapon = createNewSpecificItem(createNewBaseWeapon("Unarmed", "weapon", damage, damageInstances, range, association, apCost, Resource.objects.get(name="Books"), 1), 0, 0)

    context = {
        'attackerClass': att.sprite,
        'defenderClass': deff.sprite,
        'attWeapon': att.primaryWeapon.sprite,
        'defWeapon': deff.primaryWeapon.sprite,
        'bossPK': bossPK,
        'result' : None
    }

    return render(request, 'TheGame/battle.html', context=context)

def runBattle(request):
    if not request.method == "POST":
        messages.error(
            request,
            ('Something went wrong, please try again later'))
        return "failed to process, please use POST method"

    bossPK = request.POST.get('bossPK')

    att = getUserFromName(request)
    deff = getChampionFromID(bossPK)

    result = battle(att, deff)

    configData = json.load(open("config.json"))
    damage = configData["unarmedWeapon"]['damage']
    damageInstances = configData["unarmedWeapon"]['damageInstances']
    range = configData["unarmedWeapon"]['range']
    association = configData["unarmedWeapon"]['association']
    apCost = configData["unarmedWeapon"]['apCost']

    if att.primaryWeapon is None:
        att.primaryWeapon = createNewSpecificItem(createNewBaseWeapon("Unarmed", "weapon", damage, damageInstances, range, association, apCost, Resource.objects.get(name="Books"), 1), 0, 0)
    
    if deff.primaryWeapon is None:
        deff.primaryWeapon = createNewSpecificItem(createNewBaseWeapon("Unarmed", "weapon", damage, damageInstances, range, association, apCost, Resource.objects.get(name="Books"), 1), 0, 0)

    context = {
        'attackerClass': att.sprite,
        'defenderClass': deff.sprite,
        'attWeapon': att.primaryWeapon.sprite,
        'defWeapon': deff.primaryWeapon.sprite,
        'bossPK' : bossPK,
        'result' : result
    }
    return render(request, 'TheGame/battle.html', context=context)


def selectFaction(request):
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return redirect('createChampion')

    template = loader.get_template('TheGame/factions.html')

    resources = getAllUserResources(user)

    context = {
        "username": user.username,
        "champion": champion,
        # # item stats would replace this when item database is created
        # "damage": champion.damage,
        # "accuracy": champion.accuracy,
        # "attackSpeed": champion.attackSpeed,
        # # armour stats would replace this when armour database is created
        # "aHealth": champion.aHealth,
        # "aToughness": champion.aToughness,
        # "aEvasion": champion.aEvasion,
        "resources": resources,
    }

    output = template.render(context, request)

    return HttpResponse(output)

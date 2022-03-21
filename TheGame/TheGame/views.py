from importlib import resources
from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from Login.processes import getUserFromCookie
from TheGame.models import SpecificItem
from TheGame.processes import getAllBaseItems, getAllBosses, getChampionsItemStatPacks, getChampionsWeaponStatPacks, getUserFromName, getChampion, getChampionsItemsAndWeapons, addItemToChampion, getAllBaseItemsAndWeapons, getItemFromPK
from Resources.processes import getAllUserResources, getAllResources


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


def characterInventory(request: HttpRequest) -> HttpResponse:
    """ creates response for the character menu
    """
    if request.COOKIES.get('TheGameSessionID') is None:
        return redirect('login')

    user = getUserFromCookie(request)
    if not (champion := getChampion(user)):
        return redirect('createChampion')

    template = loader.get_template('TheGame/CharacterInventory.html')

    items = getChampionsItemsAndWeapons(champion)

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
    user = getUserFromCookie(request)

    # if not user.role == "gameMaster":
    #     return redirect('homePage')

    template = loader.get_template('TheGame/newBoss.html')

    bosses = getAllBosses()

    context = {
        "bosses": bosses,
    }

    output = template.render(context, request)

    return HttpResponse(output)


def addNewBaseItemView(request):
    """ returns html for the page for adding new items
    """

    template = loader.get_template('TheGame/addNewItemTemplate.html')

    items = getAllBaseItemsAndWeapons()
    resources = getAllResources()

    context = {
        "items": items,
        "resources" : resources
    }

    output = template.render(context, request)

    return HttpResponse(output)

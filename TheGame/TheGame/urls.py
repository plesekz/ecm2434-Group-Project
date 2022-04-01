"""TheGame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from TheGame.views import *
from . import processes, battle


urlpatterns = [
    path('admin/', admin.site.urls),
    path("/", include("Login.urls"), name='login'),
    path('qr/', include("QRC.urls")),
    path('', homePageView, name="homePage"),
    path('characterMenu/', characterMenu, name="characterMenu"),
    path('characterInventory/', characterInventory, name="characterInventory"),
    path('characterShop/', characterShop, name="characterShop"),
    path('buyPHealth/', processes.buyPHealth, name="buyPHealth"),
    path('buyPAthletics/', processes.buyPAthletics, name="buyPAthletics"),
    path('buyPBrain/', processes.buyPBrain, name="buyPBrain"),
    path('buyPControl/', processes.buyPControl, name="buyPControl"),
    path('buyItem/', processes.buyItem, name="buyItem"),
    path('equipItem/', processes.equipItem, name="equipItem"),
    path('unequipItem/', processes.unequipItem, name="unequipItem"),
    path('sellItem/', processes.sellItem, name="sellItem"),
    path('upgradeStatOnItem/', processes.upgradeStatOnItem, name="upgradeStatOnItem"),
    path('itemUpgrade/', itemUpgrade, name="itemUpgrade"),
    path('map/', map, name="map"),
    path('battleSelect/battle', battle.callBattle, name="battleSelect/battle"),
    path('login/', include("Login.urls")),
    path('battleSelect/', battleSelectView, name="battleSelect"),
    path('createChampion/', createChampionView, name='createChampion'),
    path('addBosses/', addNewBossView, name='addNewBoss'),
    path('newBossValidation', processes.addBossToSystem),
    path('addItems/', addNewBaseItemView, name="addNewItem"),
    path(
        'validateItem',
        processes.createNewBaseItemFromHTMLRequest,
        name='validateItem'),
    path('battle/', battleChampion, name="battle champion"),
    path('runbattle/', runBattle, name="runBattle"),
    path('factions/', selectFaction, name="select faction"),
        path('privacypolicy/', privacyPolicy, name="privacyPolicy"),
    path('selectfactions/', processes.selectFactions, name="selectfactions")
]

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

from TheGame.views import homePageView, characterMenu, battleSelectView
from . import processes, battle


urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr/', include("QRC.urls")),
    path('', homePageView, name="homePage"),
    path('characterMenu/', characterMenu, name="characterMenu"),
    path('buyphealth/', processes.buyPHealth, name="buyphealth"),
    path('buyptoughness/', processes.buyPToughness, name="buyptoughness"),
    path('buypevasion/', processes.buyPEvasion, name="buypevasion"),
    path('buydamage/', processes.buyDamage, name="buydamage"),
    path('buyaccuracy/', processes.buyAccuracy, name="buyaccuracy"),
    path('buyattackspeed/', processes.buyAttackSpeed, name="buyattackspeed"),
    path('buyahealth/', processes.buyAHealth, name="buyahealth"),
    path('buyatoughness/', processes.buyAToughness, name="buyatoughness"),
    path('buyaevasion/', processes.buyAEvasion, name="buyaevasion"),
    path('battleSelect/', battle.callBattle, name="battleSelect"),
    path('login/', include("Login.urls")),
    path('battleSelect/', battleSelectView, name="battleSelect"),
]

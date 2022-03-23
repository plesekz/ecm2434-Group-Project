from django.contrib import admin
from django.urls import path, include
import TheGame
from . import views
from . import processes

urlpatterns = [
    path('createRes', views.createRes),
    path('deleteRes', views.deleteRes),
    path('listRes/', views.listRes),
    path('retrieveRes/', views.retrieveRes, name="retrieveRes"),
    path('qr-landing', views.qr_landing, name="qr-landing"),
    path('manage', views.QR_management, name="manage"),
    path('newScan/', views.newScan, name="newScan")
]

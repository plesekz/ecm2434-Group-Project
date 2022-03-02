from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('createRes/', views.createRes),
    path('deleteRes/', views.deleteRes),
    path('listRes/', views.listRes),
    path('retreiveRes/', views.retrieveRes, name="retrieveRes"),
]


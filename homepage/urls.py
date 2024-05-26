from django.urls import path
from django.contrib import admin
from .views import  explore_place, explore_place_result, home

urlpatterns = [

    path('',home,name='home'),
    path('explore_place/', explore_place, name='explore_place'),
    path('explore_place_result',explore_place_result,name='explore_place_result'),
]

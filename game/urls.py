from django.urls import path
from .views import *

urlpatterns = [
    path('game_home/', game_home, name="game_home"),
]
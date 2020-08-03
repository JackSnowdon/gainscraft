from django.urls import path
from .views import *

urlpatterns = [
    path('game_home/', game_home, name="game_home"),
    path('start_new_game/', start_new_game, name="start_new_game"),
    path(r'delete_game/<int:pk>', delete_game, name="delete_game"),
]
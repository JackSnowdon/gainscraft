from django.urls import path
from .views import *

urlpatterns = [
    path('game_home/', game_home, name="game_home"),
    path('start_new_game/', start_new_game, name="start_new_game"),
    path(r'delete_game/<int:pk>', delete_game, name="delete_game"),
    path(r'transfer_points/<int:pk>/<int:value>', transfer_points, name="transfer_points"),
    path('enter_game/', enter_game, name="enter_game"),
    path('add_strengh/', add_strengh, name="add_strengh"),
    path('create_enemy/', create_enemy, name="create_enemy"),
]
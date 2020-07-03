from django.urls import path
from .views import *

urlpatterns = [
    path('workout_home/', workout_home, name="workout_home"),
    path('add_workout/', add_workout, name="add_workout"),
    path('delete_workout/<int:pk>', delete_workout, name="delete_workout"),
    path('workout_panel/<int:days>', workout_panel, name="workout_panel"),
    path('get_single_date/', get_single_date, name="get_single_date")
]
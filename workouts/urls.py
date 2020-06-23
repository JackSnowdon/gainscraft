from django.urls import path
from .views import *

urlpatterns = [
    path('workout_home/', workout_home, name="workout_home"),
    path('add_squat/', add_squat, name="add_squat"),
    path('delete_squat/<int:pk>', delete_squat, name="delete_squat"),
]
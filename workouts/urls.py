from django.urls import path
from .views import *

urlpatterns = [
    path('workout_home/', workout_home, name="workout_home"),
]
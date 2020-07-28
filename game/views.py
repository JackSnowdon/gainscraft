from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workouts.views import return_single_day, return_day_list, return_day_values
from workouts.models import *

# Create your views here.

def game_home(request):
    profile = request.user.profile
    workouts = Workout.objects.filter(done_by=profile).order_by("done_on")
    start_date = workouts[0].done_on.date()
    t = date.today()
    day_list = return_day_list(t, start_date)
    point_dict = return_day_values(day_list, workouts)
    point_total = 0
    current_streak = 0
    longest_streak = 0 
    for day, value in point_dict.items():
        point_total += value
        if value > 0:
            current_streak += 1
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 0
    return render(request, "game_home.html", {"point_total": point_total})


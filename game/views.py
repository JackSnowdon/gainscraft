from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workouts.views import return_single_day, return_day_list, return_day_values
from workouts.models import *
import math

# Create your views here.

def game_home(request):
    profile = request.user.profile
    workouts = Workout.objects.filter(done_by=profile).order_by("done_on")
    start_date = workouts[0].done_on.date()
    t = date.today()
    day_list = return_day_list(t, start_date)
    point_dict = return_day_values(day_list, workouts)
    point_base = 0
    current_streak = 0
    longest_streak = 0
    streak_bonus = 0
    for day, value in point_dict.items():
        if value > 0:
            current_streak += 1
            streak_bonus += math.floor(value * 1.125) - value
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 0
        point_base += value
    point_total = point_base + streak_bonus
    return render(request, "game_home.html", {"point_base": point_base, "longest_streak": longest_streak, "point_total": point_total, "streak_bonus": streak_bonus, "start_date": start_date })


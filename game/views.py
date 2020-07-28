from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workouts.views import return_single_day
from workouts.models import *

# Create your views here.

def game_home(request):
    profile = request.user.profile
    workouts = Workout.objects.filter(done_by=profile).order_by("-done_on")
    point_total = get_base_points(workouts)
    start_date = workouts[0].done_on.date()
    t = date.today()
    return render(request, "game_home.html", {"point_total": point_total})


# Helper Functions

def get_base_points(data):
    """ 
    takes workout data and returns all workouts as a point
    """
    amount = 0
    for d in data:
        amount += d.amount
    return amount
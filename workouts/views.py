from django.shortcuts import render
from .models import *
from datetime import date, datetime, timedelta

# Create your views here.

def workout_home(request):
    profile = request.user.profile
    squats = Squat.objects.filter(done_by=profile)
    t = date.today()
    squats_today = []
    for s in squats:
        if s.done_on.date() == t:
            squats_today.append(s)
    return render(request, "workout_home.html", {"squats": squats, "squats_today": squats_today})
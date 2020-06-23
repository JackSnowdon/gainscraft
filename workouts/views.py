from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def workout_home(request):
    profile = request.user.profile
    squats = Squat.objects.filter(done_by=profile).order_by("-done_on")
    t = date.today()
    squats_today = []
    todays_total = 0
    for s in squats:
        if s.done_on.date() == t:
            todays_total += s.amount
            squats_today.append(s)
    return render(
        request,
        "workout_home.html",
        {"squats": squats, "squats_today": squats_today, "todays_total": todays_total},
    )


@login_required
def add_squat(request):
    if request.method == "POST":
        squat_form = SquatForm()
        form = squat_form.save(commit=False)
        form.amount = int(request.POST.get("amount"))
        form.done_by = request.user.profile
        form.save()
        messages.error(request, f"{form.done_by} Added {form.amount} Squats", extra_tags="alert")
        return redirect("workout_home")

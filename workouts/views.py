from django.shortcuts import render, redirect, reverse, get_object_or_404
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
    exercises = Exercise.objects.order_by("name")
    print(exercises)
    return render(
        request,
        "workout_home.html",
        {"squats": squats, "squats_today": squats_today, "todays_total": todays_total,
        "exercises": exercises},
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


@login_required
def delete_squat(request, pk):
    this_squat = get_object_or_404(Squat, pk=pk)
    if this_squat.done_by == request.user.profile:
        this_squat.delete()
        messages.error(request, f"Deleted {this_squat.amount} Squats", extra_tags="alert")
        return redirect(reverse("workout_home"))
    else:
        messages.error(request, f"Not Your Squats!", extra_tags="alert")
        return redirect("workout_home")


@login_required
def add_workout(request):
    if request.method == "POST":
        workout_form = WorkoutForm()
        form = workout_form.save(commit=False)
        form.amount = int(request.POST.get("amount"))
        form.workout_type = get_object_or_404(Exercise, name=request.POST.get("commit"))
        form.done_by = request.user.profile
        form.save()
        messages.error(request, f"{form.done_by} Added {form.amount} {form.workout_type}s", extra_tags="alert")
        return redirect("workout_home")
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
    t = date.today()
    exercises = Exercise.objects.order_by("name")
    squats = []
    squats_today = 0
    press_ups = []
    press_ups_today = 0
    sit_ups = []
    sit_ups_today = 0
    workouts = Workout.objects.filter(done_by=profile).order_by("-done_on")
    for w in workouts:
        if w.workout_type.name == "Squat" and w.done_on.date() == t:
            squats_today += w.amount
            squats.append(w)
        elif w.workout_type.name == "Press Up" and w.done_on.date() == t:
            press_ups_today += w.amount
            press_ups.append(w)
        elif w.workout_type.name == "Sit Up" and w.done_on.date() == t:
            sit_ups_today += w.amount
            sit_ups.append(w)
    return render(
        request,
        "workout_home.html",
        {
            "exercises": exercises,
            "squats": squats,
            "squats_today": squats_today,
            "press_ups": press_ups,
            "press_ups_today": press_ups_today,
            "sit_ups": sit_ups,
            "sit_ups_today": sit_ups_today,
        },
    )


@login_required
def add_workout(request):
    if request.method == "POST":
        workout_form = WorkoutForm()
        form = workout_form.save(commit=False)
        if request.POST.get("amount") == "":
            messages.error(
                request,
                f"Invalid Input",
                extra_tags="alert",
            )
        else:
            form.amount = int(request.POST.get("amount"))
            form.workout_type = get_object_or_404(Exercise, name=request.POST.get("commit"))
            form.done_by = request.user.profile
            form.save()
            messages.error(
                request,
                f"{form.done_by} Added {form.amount} {form.workout_type}s",
                extra_tags="alert",
            )
        return redirect("workout_home")


@login_required
def delete_workout(request, pk):
    this_workout = get_object_or_404(Workout, pk=pk)
    if this_workout.done_by == request.user.profile:
        this_workout.delete()
        messages.error(
            request, f"Deleted {this_workout.amount} {this_workout.workout_type}", extra_tags="alert"
        )
        return redirect(reverse("workout_home"))
    else:
        messages.error(request, f"Not Your Squats!", extra_tags="alert")
        return redirect("workout_home")


@login_required
def workout_panel(request):
    profile = request.user.profile
    workouts = Workout.objects.filter(done_by=profile).order_by("-done_on")
    return render(request, "workout_panel.html")
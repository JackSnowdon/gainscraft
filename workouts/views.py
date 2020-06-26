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
    exercises = Exercise.objects.order_by("name")
    workouts = Workout.objects.filter(done_by=profile).order_by("-done_on")
    squats, squats_today = return_single_day(workouts, "Squat", 0)
    press_ups, press_ups_today = return_single_day(workouts, "Press Up", 0)
    sit_ups, sit_ups_today = return_single_day(workouts, "Sit Up", 0)
    _, squats_yesterday = return_single_day(workouts, "Squat", 1)
    _, press_ups_yesterday = return_single_day(workouts, "Press Up", 1)
    _, sit_ups_yesterday = return_single_day(workouts, "Sit Up", 1)
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
            "squats_yesterday": squats_yesterday,
            "press_ups_yesterday": press_ups_yesterday,
            "sit_ups_yesterday": sit_ups_yesterday,
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
    tw_squats, tw_squats_total = return_range_of_dates(workouts, "Squat", 0, 7)
    tw_situps, tw_situps_total = return_range_of_dates(workouts, "Sit Up", 0, 7)
    tw_pressups, tw_pressups_total = return_range_of_dates(workouts, "Press Up", 0, 7)
    t = date.today()
    start_of_tw = t - timedelta(days=7)
    return render(request, "workout_panel.html", {
            "tw_squats": tw_squats,
            "tw_squats_total": tw_squats_total,
            "tw_situps": tw_situps,
            "tw_situps_total": tw_situps_total,
            "tw_pressups": tw_pressups,
            "tw_pressups_total": tw_pressups_total,
            "t": t,
            "start_of_tw": start_of_tw,
        })


# Helper Functions 


def return_single_day(data, excerise, time):
    """
    Takes data(django filter set)
    excerise as string(Squat, Press Up, Sit Up)
    time int(0 = today, 1 = yesterday)

    returns filtered data set and daily amount
    """
    t = date.today()
    y = t - timedelta(days=time)
    total_amount = 0
    exce = data.filter(workout_type__name=excerise, done_on__date=y)
    for e in exce:
        total_amount += e.amount
    return exce, total_amount


def return_range_of_dates(data, excerise, start, end):
    """
    Takes data(django filter set)
    excerise as string(Squat, Press Up, Sit Up)
    start int(-1)
    end (int+1)

    returns filtered data set and daily amount
    """
    t = date.today()
    start_date = t - timedelta(days=start-1)
    end_date = start_date - timedelta(days=end + 1)
    amount = 0
    dataset = data.filter(workout_type__name=excerise, done_on__range=(end_date, start_date))
    for d in dataset:
        amount += d.amount
    return dataset, amount
    
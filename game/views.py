from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from .forms import *
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
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
    transfer_amount = 0
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
    try:
        game_profile = profile.game_base
    except ObjectDoesNotExist:
        game_profile = None
    else: 
        game_profile = profile.game_base
        transfer_amount = point_total - game_profile.cashed_in_amount
    return render(request, "game_home.html", {"point_base": point_base, "longest_streak": longest_streak, "point_total": point_total, "streak_bonus": streak_bonus, "start_date": start_date, "game_profile": game_profile, "transfer_amount": transfer_amount })


@login_required
def start_new_game(request):
    if request.method == "POST":
        game_form = StartGameForm(request.POST)
        if game_form.is_valid():
            form = game_form.save(commit=False)
            form.done_by = request.user.profile
            form.save()
            messages.error(request, "Started {0}".format(form.name), extra_tags="alert")
            return redirect("game_home")
    else:
        game_form = StartGameForm()
    return render(request, "start_new_game.html", {"game_form": game_form})


@login_required
def delete_game(request, pk):
    this_game = get_object_or_404(GameBase, pk=pk)
    if this_game.done_by == request.user.profile:
        this_game.delete()
        messages.error(
            request, f"Deleted {this_game}", extra_tags="alert"
        )
        return redirect(reverse("game_home"))
    else:
        messages.error(request, f"Not Your Game!", extra_tags="alert")
        return redirect("game_home")


@login_required
def transfer_points(request, pk, value):
    this_game = get_object_or_404(GameBase, pk=pk)
    if this_game.done_by == request.user.profile:
        this_game.current_points += value
        this_game.cashed_in_amount += value
        this_game.save()
        return redirect(reverse("game_home"))
    else:
        messages.error(request, f"Not Your Game!", extra_tags="alert")
        return redirect("game_home")

        
@login_required
def enter_game(request):
    profile = request.user.profile
    game_profile = profile.game_base
    strengh_cost = get_upgrade_amount(game_profile)
    return render(request, "enter_game.html", {"game_profile": game_profile, "strengh_cost": strengh_cost})


@login_required
def add_strengh(request):
    profile = request.user.profile
    game_profile = profile.game_base
    cost = get_upgrade_amount(game_profile)
    if game_profile.current_points >= cost:
        game_profile.current_points -= cost
        game_profile.strengh += 1
        game_profile.save()
        messages.error(request, f"Upped Strengh By 1 ({cost})", extra_tags="alert")
    else:
        messages.error(request, f"You Need {cost}!", extra_tags="alert")
    return redirect("enter_game")


@login_required
def create_enemy(request):
    profile = request.user.profile
    if request.method == "POST":
        if profile.game_base.target:
            profile.game_base.target.delete()
        enemy_form = NewEnemyForm(request.POST)
        if enemy_form.is_valid():
            form = enemy_form.save(commit=False)
            form.max_hp = form.level * 100
            form.current_hp = form.max_hp
            form.strengh = form.level * 2
            form.xp = form.level * 10
            form.fighting = profile.game_base
            form.save()
            messages.error(request, f"Created {form.name}", extra_tags="alert")
            return redirect("enter_game")
    else:
        enemy_form = NewEnemyForm()
    return render(request, "create_enemy.html", {"enemy_form": enemy_form})


# Helper Functions


def get_upgrade_amount(profile):
    return math.floor(100 + (profile.strengh * 1.175))
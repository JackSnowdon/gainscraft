from django.shortcuts import render
from .models import *

# Create your views here.

def workout_home(request):
    profile = request.user.profile
    squats = Squat.objects.filter(done_by=profile)
    return render(request, "workout_home.html", {"squats": squats})
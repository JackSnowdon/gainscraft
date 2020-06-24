from django import forms
from .models import *

class SquatForm(forms.ModelForm):

    class Meta:
        model = Squat
        fields = ['amount']


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ['amount', 'workout_type']
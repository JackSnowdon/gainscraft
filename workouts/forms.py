from django import forms
from .models import *

class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ['amount', 'workout_type']


class SingleDateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#singledatepicker'
        })
    )
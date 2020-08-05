from django import forms
from .models import *

class StartGameForm(forms.ModelForm):

    class Meta:
        model = GameBase
        fields = ['name']


class NewEnemyForm(forms.ModelForm):

    class Meta:
        model = Enemy
        fields = ['name', 'level']
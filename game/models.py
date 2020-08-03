from django.db import models
from accounts.models import Profile

# Create your models here.

class GameBase(models.Model):
    name = models.CharField(max_length=255)
    done_by = models.OneToOneField(Profile, related_name='game_base', on_delete=models.PROTECT)
    current_points = models.IntegerField(default=0)
    cashed_in_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


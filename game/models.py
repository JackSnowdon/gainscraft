from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import Profile

# Create your models here.

class GameBase(models.Model):
    name = models.CharField(max_length=255)
    done_by = models.OneToOneField(Profile, related_name='game_base', on_delete=models.PROTECT)
    current_points = models.IntegerField(default=0)
    cashed_in_amount = models.IntegerField(default=0)
    level = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=1)
    strengh = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=1)
    xp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000000)], default=1)
    kills = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000000)], default=0)

    def __str__(self):
        return self.name


class Enemy(models.Model):
    name = models.CharField(max_length=255)
    current_hp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000000)], default=1)
    max_hp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000000)], default=1)
    level = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=1)
    strengh = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=1)
    xp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000000)], default=1)
    fighting = models.OneToOneField(GameBase, related_name='target', on_delete=models.PROTECT)

    def __str__(self):
        return self.name



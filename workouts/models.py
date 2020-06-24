from django.db import models
from accounts.models import Profile

# Create your models here.

class Squat(models.Model):
    amount = models.IntegerField(default=0)
    done_on = models.DateTimeField(auto_now_add=True)
    done_by = models.ForeignKey(Profile, related_name='squats', on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.done_by} Squats {self.amount} Times At {self.done_on}"


class Exercise(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Workout(models.Model):
    amount = models.IntegerField(default=0)
    done_on = models.DateTimeField(auto_now_add=True)
    done_by = models.ForeignKey(Profile, related_name='workout', on_delete=models.PROTECT)
    workout_type = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.done_by} Did {self.workout_type.name} {self.amount} Times At {self.done_on}"


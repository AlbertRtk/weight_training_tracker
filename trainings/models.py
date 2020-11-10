from django.db import models

# Create your models here.
class Training(models.Model):
    name = 'My weight trainig'
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)


class Exercise(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    name = models.TextField(default='Exercise')
    weight_kg = models.FloatField(blank=True, null=True)
    weight_per = models.TextField(blank=True, null=True)
    series = models.IntegerField(blank=True, null=True)  # max 4
    reps_s1 = models.IntegerField(blank=True, null=True)
    reps_s2 = models.IntegerField(blank=True, null=True)
    reps_s3 = models.IntegerField(blank=True, null=True)
    reps_s4 = models.IntegerField(blank=True, null=True)

from django.db import models


class Training(models.Model):
    name = models.TextField(default='My weight training')
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)


class Exercise(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    name = models.TextField(default='Exercise')
    weight_kg = models.FloatField(blank=True, null=True)
    weight_per = models.TextField(blank=True, null=True)
    series = models.IntegerField(blank=True, null=True)
    reps = models.JSONField(blank=True, null=True)


class TrainingPlan(models.Model):
    name = models.TextField(unique=True)
    exercises = models.JSONField()

    '''
    e.g.
    [{'name': 'pushup', 'weight_kg': 5, 'weight_per': 'total'}]
    '''

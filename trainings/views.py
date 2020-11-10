from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Training, Exercise
from datetime import datetime


def trainings_view(request):
    all_trainings = Training.objects.all()
    return render(
        request, 
        'trainings.html', 
        {'all_trainings': all_trainings}
        )
    

def single_training_view(request, training_id):
    training = Training.objects.get(id=training_id)
    return render(
        request, 
        'single-training.html', 
        {'training': training}
        )


def record_training(request):
    new_training = Training()
    new_training.save()
    training_id = new_training.id
    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def edit_training_view(request, training_id):
    training = Training.objects.get(id=training_id)
    exercises = Exercise.objects.filter(training__id=training_id)
    return render(
        request,
        'edit-training.html',
        {'training': training, 'exercises': exercises}
    )


def start_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.time_start = datetime.now()
    training.save()
    return HttpResponseRedirect(f'/edit-training/{training_id}/')
    

def stop_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.time_end = datetime.now()
    training.save()
    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def save_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.save()
    return HttpResponseRedirect(f'/trainings/{training_id}/')


def cancel_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.delete()
    return HttpResponseRedirect('/trainings/')


def add_exercise_to_training(request, training_id):
    training = Training.objects.get(id=training_id)
    exercise = Exercise()
    exercise.training = training
    exercise.save()
    return HttpResponseRedirect(f'/edit-training/{training_id}/')

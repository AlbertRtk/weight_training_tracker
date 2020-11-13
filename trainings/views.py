from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Training, Exercise, TrainingPlan
from django.utils import timezone
from django.db.models import Sum


def trainings_view(request):
    all_trainings = Training.objects.all()
    all_trainings = all_trainings[::-1]
    return render(
        request, 
        'trainings.html', 
        {'all_trainings': all_trainings}
        )
    

def single_training_view(request, training_id):
    training = Training.objects.get(id=training_id)
    exercises = Exercise.objects.filter(training__id=training_id)
    return render(
        request, 
        'single-training.html', 
        {'training': training, 'exercises': exercises}
        )


def record_training(request):
    new_training = Training()
    new_training.save()
    return HttpResponseRedirect(f'/edit-training/{new_training.id}/')


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
    training.time_start = timezone.now()
    training.save()
    return HttpResponseRedirect(f'/edit-training/{training_id}/')
    

def stop_training(request, training_id):
    # save the end time
    training = Training.objects.get(id=training_id)
    training.time_end = timezone.now()
    training.duration = training.time_end - training.time_start
    training.save()

    # make sure to save all exercises and progress
    exercises = Exercise.objects.filter(training__id=training_id)
    for exercise in exercises:
        exercise.name = request.POST[f'name_{exercise.id}']
        exercise.weight_kg = request.POST[f'weight_kg_{exercise.id}']
        exercise.weight_per = request.POST[f'weight_per_{exercise.id}']

        # read and save reps in all series
        for s in exercise.reps:
            exercise.reps[s] = request.POST[f'rep_{s}']

        exercise.save()

    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def save_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.save()
    # exercises have been already saved in stop_training
    return HttpResponseRedirect(f'/trainings/{training_id}/')


def cancel_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.delete()
    # exercises in the training will be deleted to (Foreign Key - CASCADE)
    return HttpResponseRedirect('/trainings/')


def add_exercise_to_training(request, training_id):
    training = Training.objects.get(id=training_id)
    exercise = Exercise()

    exercise.training = training
    exercise.name = request.POST['name']
    exercise.weight_kg = request.POST['weight_kg']
    exercise.weight_per = request.POST['weight_per']
    exercise.series = request.POST['series']
    exercise.reps = dict()

    """ Html form displays all sereis for all exercises in the training 
        therefore we need unique keys for each of the reps series. Before 
        setting the keys for reps series, cout total number of the series
        in the training and use the sum as the starting id for series 
        in next exercise. """
    this_training_exercises = Exercise.objects.filter(training__id=training_id)
    series_count = this_training_exercises.aggregate(Sum('series'))['series__sum']
    series_count = series_count if series_count else 0
    for s in range(series_count, series_count+int(exercise.series)):
        exercise.reps[s] = 0

    exercise.save()

    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def save_training_plan(request, training_id):
    training_plan = TrainingPlan()
    plan_table = []
    
    exercises = Exercise.objects.filter(training__id=training_id)
    for exercise in exercises:
        plan_table.append(
            {
                'name': request.POST[f'name_{exercise.id}'],
                'weight_kg': request.POST[f'weight_kg_{exercise.id}'],
                'weight_per': request.POST[f'weight_per_{exercise.id}']
            }
        )

    training_plan.name = 'My training plan'  # https://www.w3schools.com/howto/howto_js_collapsible.asp
    training_plan.exercises = plan_table
    training_plan.save()

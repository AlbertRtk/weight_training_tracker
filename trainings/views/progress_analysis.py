from django.shortcuts import render
from trainings.models import Exercise
from plotly.offline import plot
import plotly.graph_objects as go


def progress_analysis_view(request):
    all_exercises_names = Exercise.objects.values('name').distinct()
    
    if all_exercises_names:
    
        exercise_name = request.POST.get('select_exercise_name', None)

        if exercise_name is None:
            exercise_name = all_exercises_names[0]['name']

        data = get_exercise_summary_in_dict(exercise_name)
        plot_div = get_progress_plot(data, exercise_name)

    else:
        plot_div = None
        exercise_name = None
        all_exercises_names = None

    return render(request, 'progress-analysis.html', 
                  context={'plot_div': plot_div, 
                           'exercises_names': all_exercises_names,
                           'selected_exercise_name': exercise_name})


def get_progress_plot(data, exercise_name):
    # scale factor for marker size in the graph
    # marker_size = marker_factor * exercise.weight
    marker_factor = 5

    if all(data['Weight']):
        marker_size = [marker_factor*w for w in data['Weight']]
    else: 
        marker_size = [marker_factor*marker_factor for _ in data['Weight']]

    figs = []

    # collect plots for all reps in on array
    for k, val in data['Reps'].items():
        figs.append(
            go.Scatter(x=data['Date'], 
                       y=val,
                       mode='markers', 
                       opacity=0.8,
                       marker_size=marker_size,
                       hovertext=data['Weight'],
                       hovertemplate='Date: %{x} <br>Reps: %{y} <br>Weight: %{hovertext} kg',
                       name='Series '+k)
        )

    # layout settings
    layout = {
        'title': exercise_name,
        'yaxis_title': 'Repetitions',
        'height': 600,
        }

    return plot({'data':figs, 'layout': layout}, output_type='div')


def get_exercise_summary_in_dict(exercise_name):
    exercises = Exercise.objects.filter(name=exercise_name)

    # dict with data to plot
    data = {'Date': [], 'Reps': {}, 'Weight': []}

    for ex in exercises:
        data['Date'].append(ex.training.time_start.date())
        data['Weight'].append(ex.weight_kg)

        reps = list(ex.reps.values())

        for i, r in enumerate(reps, 1):
            if str(i) in data['Reps'].keys():
                data['Reps'][str(i)].append(int(r))
            else:
                data['Reps'][str(i)] = [int(r)]
    
    return data

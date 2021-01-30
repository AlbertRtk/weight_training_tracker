from django.shortcuts import render
from trainings.models import Exercise
from plotly.offline import plot
import plotly.graph_objects as go


def progress_analysis_view(request):
    all_exercises_names = Exercise.objects.values('name').distinct()
    exercise_name = None 
    progress_plot_div = ''
    total_reps_plot_div = ''
    weight_plot_div = ''
    
    if all_exercises_names:
    
        exercise_name = request.POST.get('select_exercise_name', None)

        if exercise_name is None:
            exercise_name = all_exercises_names[0]['name']

        data = get_exercise_summary_in_dict(exercise_name)

        progress_plot_div = get_progress_plot(data, exercise_name)
        total_reps_plot_div = get_total_reps_plot(data, exercise_name)

        if any(data['Weight']):
            weight_plot_div = get_weight_plot(data, exercise_name)

  

    return render(request, 'progress-analysis.html', 
                  context={'progress_plot_div': progress_plot_div, 
                           'weight_plot_div': weight_plot_div,
                           'total_reps_plot_div': total_reps_plot_div,
                           'exercises_names': all_exercises_names})


def get_progress_plot(data, exercise_name):
    # scale factor for marker size in the graph
    # marker_size = marker_factor * exercise.weight
    marker_factor = 5

    if all(data['Weight']):
        if any([w>marker_factor**2 for w in data['Weight']]):
            # avoiding too big markers
            marker_factor = marker_factor * marker_factor / data['Weight'][0]
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
        'height': 500,
        'xaxis_range': [data['Date'][0], data['Date'][-1]],
        'margin': dict(b=25, r=0),
        'legend': dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0.0)
        }

    return plot({'data':figs, 'layout': layout}, output_type='div')


def get_weight_plot(data, exercise_name):
    figs = []

    # 
    figs = [
        go.Scatter(x=data['Date'], 
                   y=data['Weight'],
                   mode='lines+markers', 
                   opacity=1,
                   hovertext=data['Weight'],
                   hovertemplate='Date: %{x} <br>Weight: %{hovertext} kg')
    ]

    # layout settings
    layout = {
        'yaxis_title': 'Weight / kg',
        'height': 200,
        'xaxis_range': [data['Date'][0], data['Date'][-1]],
        'margin': dict(t=25, b=25, r=0)
        }

    return plot({'data':figs, 'layout': layout}, output_type='div')


def get_total_reps_plot(data, exercise_name):
    total_reps = []
    
    # counting reps per training
    for z in zip(*data['Reps'].values()):
        total_reps.append(sum(z))

    # 
    figs = [
        go.Bar(x=data['Date'], 
               y=total_reps, 
               opacity=1,
               hovertext=data['Weight'],
               hovertemplate='Date: %{x} <br>Total reps: %{y} <br>Weight: %{hovertext} kg')
    ]

    # layout settings
    layout = {
        'yaxis_title': 'Total reps count',
        'height': 200,
        'margin': dict(t=25, b=25, r=0)
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

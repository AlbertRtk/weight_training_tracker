from django.shortcuts import render
from .models import Training

# Create your views here.
def trainingsView(request):
    all_trainings = Training.objects.all()
    return render(request, 'trainings.html', {'all_trainings': all_trainings})
    
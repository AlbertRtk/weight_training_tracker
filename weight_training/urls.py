"""weight_training URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from trainings.views import trainings_view, single_training_view, \
    edit_training_view, start_training, stop_training, save_training, \
    cancel_training, record_training, add_exercise_to_training, \
    save_training_plan, load_training_plan


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trainings.urls')),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.achievement_view, name='Create Achievement'),
]
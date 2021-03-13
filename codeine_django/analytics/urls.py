from django.urls import path

from . import views

urlpatterns = [
    # ticket views
    path('', views.post_log_view, name='Create Event Log'),
]

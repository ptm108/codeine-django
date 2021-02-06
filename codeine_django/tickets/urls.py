from django.urls import path

from . import views_tickets

urlpatterns = [
    # ticket views
    path('/', views_tickets.ticket_view, name='Get all tickets')
]

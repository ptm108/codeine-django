from django.urls import path

from . import views_tickets

urlpatterns = [
    # ticket views
    path('', views_tickets.ticket_view, name='Get all tickets'),
    path('<slug:pk>', views_tickets.single_ticket_view, name="Get Ticket, Update Ticket Details, Delete Ticket"),
    path('<slug:pk>/resolve', views_tickets.resolve_ticket_view, name='Resolve ticket')
]

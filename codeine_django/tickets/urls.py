from django.urls import path

from . import views_tickets, views_ticket_messages

urlpatterns = [
    # ticket views
    path('/ticket', views_tickets.ticket_view, name='Create ticket, Get all/Search tickets'),
    path('/ticket/<slug:pk>', views_tickets.single_ticket_view, name="Get Ticket, Update Ticket Details, Delete Ticket"),
    path('/ticket/<slug:pk>/resolve', views_tickets.resolve_ticket_view, name='Admin resolves ticket'),

    # ticket message views
    path('/messages', views_ticket_messages.ticket_message_view, name='Create ticket message, Get all/Search ticket messages'),
    path('/messages/<slug:pk>', views_ticket_messages.single_ticket_message_view, name='Get ticket message')
]

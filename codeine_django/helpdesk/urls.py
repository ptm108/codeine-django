from django.urls import path

from . import views_tickets, views_ticket_messages

urlpatterns = [
    # ticket views
    path('/tickets', views_tickets.ticket_view, name='Create ticket, Get all/Search tickets'),
    path('/tickets/<slug:pk>', views_tickets.single_ticket_view, name="Get Ticket, Delete Ticket"),
    path('/tickets/<slug:pk>/resolve', views_tickets.resolve_ticket_view, name='Admin resolves ticket'),

    # ticket message views
    path('/tickets/<slug:ticket_id>/messages', views_ticket_messages.ticket_message_view, name='Create ticket message, Get all/Search ticket messages by ticket'),
    path('/messages/<slug:pk>', views_ticket_messages.single_ticket_message_view, name='Get ticket message')
]

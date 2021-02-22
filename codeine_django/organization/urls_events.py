from django.urls import path

from . import views_event, views_event_application, views_event_payment

urlpatterns = [
    # event views
    path('', views_event.event_view, name='Create/Get all/Search Event'),
    path('/<slug:pk>', views_event.single_event_view, name='Read/update/delete for Event'),
    path('/<slug:pk>/cancel', views_event.cancel_event, name='Partner cancels Event'),

    # event application views
    path('/<slug:event_id>/apply', views_event_application.event_application_view, name='Member apply for Event, Get/Search applications for this Event'),
    path('/application/<slug:pk>', views_event_application.single_event_application_view, name='Get event application by id'),
    path('/application/<slug:pk>/cancel', views_event_application.cancel_event_application, name='Member cancels event application'),
    path('/organization/applications', views_event_application.partner_event_application_view, name='Partner Get/ Search event applications for their own organization'),
]

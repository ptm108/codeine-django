from django.urls import path

from . import views_event, views_event_application, views_event_payment

urlpatterns = [
    # event views
    path('', views_event.event_view, name='Create/Get all/Search Event'),
    path('/<slug:pk>', views_event.single_event_view, name='Read/update/delete for Event'),
    path('/<slug:pk>/cancel', views_event.cancel_event, name='Partner cancels Event'),
]

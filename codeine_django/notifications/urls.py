from django.urls import path

from . import views_notifications

urlpatterns = [
    # notification views
    path('notifications', views_notifications.notification_view,
         name='Get all/Search Notifications'),
    path('notifications/<slug:pk>', views_notifications.single_notification_view,
         name='Read/Update/Delete Notificaiton'),
]
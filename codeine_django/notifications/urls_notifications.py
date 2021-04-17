from django.urls import path

from . import views_notifications

urlpatterns = [
    # notification views
    path('', views_notifications.notification_view,
         name='Get all/Search Notifications'),
    path('/<slug:pk>', views_notifications.single_notification_view,
         name='Read or Delete Notificaiton'),
]

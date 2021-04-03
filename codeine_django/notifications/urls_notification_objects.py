from django.urls import path

from . import views_notification_objects

urlpatterns = [
    # notification views
    path('', views_notification_objects.notification_object_view,
         name='Get all/Search Notifications'),
    path('/<slug:pk>', views_notification_objects.single_notification_object_view,
         name='Read or Delete Notificaiton'),
    path('/<slug:pk>/read', views_notification_objects.mark_notification_as_read,
         name='Mark notification object as read'),
    path('/<slug:pk>/unread', views_notification_objects.mark_notification_as_unread,
         name='Mark notification object as unread'),
    path('/mark/multiple-read', views_notification_objects.mark_multiple_as_read,
         name="Mark multiple notification objects as read"),
    path('/mark/multiple-unread', views_notification_objects.mark_multiple_as_unread,
         name="Mark multiple notification objects as unread"),
    path('/mark/all-read', views_notification_objects.mark_all_as_read,
         name="Mark all notification objects as read"),
    path('/mark/all-unread', views_notification_objects.mark_all_as_unread,
         name="Mark all notification objects as unread"),
]

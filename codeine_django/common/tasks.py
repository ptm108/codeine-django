from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.schedules import crontab
from codeine_django.celery import app

from notifications.models import Notification, NotificationObject
from .models import BaseUser


@shared_task
def subscription_reminder(base_user_id):
    base_user = BaseUser.objects.get(pk=base_user_id)

    title = f'Your subscription is ending soon!'
    description = f'A reminder that your Membership Subscription is ending in 7 days. Extend now!'
    notification_type = 'GENERAL'
    notification = Notification(
        title=title, description=description, notification_type=notification_type)
    notification.save()
    notification_object = NotificationObject(receiver=base_user, notification=notification)
# end def

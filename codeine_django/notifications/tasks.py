from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.schedules import crontab
from codeine_django.celery import app

from common.models import Partner
from .models import Notification, NotificationObject

@shared_task
def weekly_notification():
    partners = Partner.objects.all()
    title = f'It is the start of the new week!'
    description = f'Checkout the analytics page for the past week'
    notification_type = 'GENERAL'
    notification = Notification(
        title=title, description=description, notification_type=notification_type)
    notification.save()

    for partner in partners:
        notification_object = NotificationObject(receiver=partner.user, notification=notification)
        notification_object.save()
    # end for
# end def

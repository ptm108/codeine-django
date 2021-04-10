from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.schedules import crontab
from codeine_django.celery import app

from notifications.models import Notification, NotificationObject
from .models import ConsultationSlot, ConsultationApplication


@shared_task
def consultation_slot_reminder(consultation_slot_id):
    consultation_slot = ConsultationSlot.objects.get(pk=consultation_slot_id)
    partner = consultation_slot.partner

    title = f'Your consultation is starting soon!'
    description = f'A reminder that your consultation {consultation_slot.title} is starting in 30 minutes!'
    notification_type = 'CONSULTATION'
    notification = Notification(
        title=title, description=description, notification_type=notification_type, consultation_slot=consultation_slot)
    notification.save()
    notification_object = NotificationObject(receiver=partner.user, notification=notification)
    notification_object.save()
# end def


@shared_task
def consultation_application_reminder(consultation_application_id):
    consultation_application = ConsultationApplication.objects.get(pk=consultation_application_id)
    consultation_slot = consultation_application.consultation_slot
    member = consultation_application.member

    title = f'Your consultation is starting soon!'
    description = f'A reminder that your consultation {consultation_slot.title} is starting in 30 minutes!'
    notification_type = 'CONSULTATION'
    notification = Notification(
        title=title, description=description, notification_type=notification_type, consultation_slot=consultation_slot)
    notification.save()
    notification_object = NotificationObject(receiver=member.user, notification=notification)
    notification_object.save()
# end def

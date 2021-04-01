from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import TicketMessage
from courses.models import Course, Enrollment
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=TicketMessage)
def update_ticket_message(sender, instance, created, **kwargs):
    ticket = instance.ticket

    if created:
        title = f'New reply for ticket {ticket}!'
        description = f'{instance.message}'
        notification_type = 'HELPDESK'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, ticket=ticket)
        notification.save()

        receiver = ticket.base_user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def

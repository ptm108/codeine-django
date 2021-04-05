from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import TicketMessage
from common.models import BaseUser
from courses.models import Course, Enrollment
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=TicketMessage)
def update_ticket_message(sender, instance, created, **kwargs):
    ticket = instance.ticket

    if created:
        sender = instance.base_user
        ticket_owner = instance.ticket.base_user
        participant_ids = TicketMessage.objects.filter(
            ticket=instance.ticket).values_list('base_user', flat=True).distinct()
        title = f'Helpdesk: New reply for {ticket.description}!'
        description = f'{instance.message}'
        notification_type = 'HELPDESK'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, ticket=ticket)
        notification.save()

        for participant_id in participant_ids:
            if sender.id != participant_id:
                receiver = BaseUser.objects.get(pk=participant_id)
                notification_object = NotificationObject(
                    receiver=receiver, notification=notification)
                notification_object.save()
            # end if
        # end for
    # end if
# end def

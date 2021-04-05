from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TicketMessage, Ticket
from common.models import BaseUser
from courses.models import Course, Enrollment
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=TicketMessage)
def update_ticket_message(sender, instance, created, **kwargs):
    ticket = instance.ticket

    if created:
        sender = instance.base_user
        ticket = instance.ticket
        ticket_owner = ticket.base_user
        participant_ids = TicketMessage.objects.filter(
            ticket=instance.ticket).order_by().values_list('base_user', flat=True).distinct()
        title = f''
        try:
            if ticket.transaction:
                title = f'Helpdesk: New reply for Transaction Enquiry!'
            if ticket.course:
                title = f'Helpdesk: New reply for Enquiry about Course {ticket.course.title}!'
            if ticket.article:
                title = f'Helpdesk: New reply for Enquiry about Article {ticket.article.title}!'
            if ticket.industry_project:
                title = f'Helpdesk: New reply for Enquiry about Industry Project {ticket.industry_project.title}!'
            if ticket.consultation_slot:
                title = f'Helpdesk: New reply for Enquiry about Consultation Slot {ticket.consultation_slot.title}!'
            if ticket.code_review:
                title = f'Helpdesk: New reply for Enquiry about Code Review {ticket.code_review.title}!'
            # end ifs

            description = f'{instance.message}'
            notification_type = 'HELPDESK'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, ticket=ticket)
            notification.save()

            if sender.id != ticket_owner.id:
                notification_object = NotificationObject(
                    receiver=ticket_owner, notification=notification)
                notification_object.save()
            # end if

            for participant_id in participant_ids:
                if ticket_owner.id != participant_id:
                    if sender.id != participant_id:
                        receiver = BaseUser.objects.get(pk=participant_id)
                        notification_object = NotificationObject(
                            receiver=receiver, notification=notification)
                        notification_object.save()
                    # end if
                # end if
            # end for
        except:
            print('error')
        # end try-except
    # end if
# end def



@receiver(post_save, sender=Ticket)
def update_ticket_message(sender, instance, created, **kwargs):
    if created:
        title = f''
        try:
            if instance.transaction:
                title = f'Helpdesk: New Transaction Enquiry created!'
            if instance.course:
                title = f'Helpdesk: New Enquiry about Course {instance.course.title} created!'
            if instance.article:
                title = f'Helpdesk: New Enquiry about Article {instance.article.title} created!'
            if instance.industry_project:
                title = f'Helpdesk: New Enquiry about Industry Project {instance.industry_project.title}!'
            if instance.consultation_slot:
                title = f'Helpdesk: New Enquiry about Consultation Slot {instance.consultation_slot.title}!'
            if instance.code_review:
                title = f'Helpdesk: New Enquiry about Code Review {instance.code_review.title}!'
            # end ifs

            description = f'{instance.description}'
            notification_type = 'HELPDESK'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, ticket=instance)
            notification.save()

            admins = BaseUser.objects.filter(is_admin=True)

            for admin in admins:
                notification_object = NotificationObject(
                    receiver=admin, notification=notification)
                notification_object.save()
            # end for
        except:
            print('error')
        # end try-except
    # end if
# end def

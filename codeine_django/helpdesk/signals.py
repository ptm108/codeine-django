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
        ticket = instance.ticket
        ticket_owner = ticket.base_user
        ticket_admin = ticket.assigned_admin
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

            print(ticket.ticket_type)
            if ticket.ticket_type == 'ACCOUNT':
                title = f'Helpdesk: New reply for Enquiry about your Account!'
            if ticket.ticket_type == 'GENERAL':
                title = f'Helpdesk: New reply for your General Enquiry!'
            if ticket.ticket_type == 'TECHNICAL':
                title = f'Helpdesk: New reply for your Technical Enquiry!'

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

            if ticket_admin:
                if sender.id != ticket_admin.id:
                    notification_object = NotificationObject(
                        receiver=ticket_admin, notification=notification)
                    notification_object.save()
                # end if
            # end if

            # for participant_id in participant_ids:
            #     if ticket_owner.id != participant_id:
            #         if sender.id != participant_id:
            #             receiver = BaseUser.objects.get(pk=participant_id)
            #             notification_object = NotificationObject(
            #                 receiver=receiver, notification=notification)
            #             notification_object.save()
            #         # end if
            #     # end if
            # # end for
        except:
            print('error')
        # end try-except
    # end if
# end def

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ConsultationApplication, ConsultationSlot
from courses.models import Course, Enrollment
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=ConsultationApplication)
def update_consultation_application(sender, instance, created, **kwargs):
    consultation_slot = instance.consultation_slot
    partner = consultation_slot.partner

    if created:
        title = f'New application for your consultation slot {consultation_slot.title}!'
        description = f'New application for consultation slot {consultation_slot.title} made by {instance.member.user.first_name} {instance.member.user.last_name}'

        notification_type = 'CONSULTATION'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, consultation_slot=consultation_slot)
        notification.save()

        receiver = partner.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


@receiver(post_save, sender=ConsultationSlot)
def update_consultation_slot(sender, instance, created, **kwargs):
    consultation_slot = instance
    partner = instance.partner

    if created:
        title = f'New consultation slot {consultation_slot.title} available!'
        notification_type = 'CONSULTATION'

        courses = Course.objects.filter(partner=partner)
        for course in courses:
            description = f'New consultation slot {consultation_slot.title} available by the instructor of {course.title}!'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, consultation_slot=consultation_slot)
            notification.save()
            print('in courses')
            enrollments = Enrollment.objects.filter(course=course)
            for enrollment in enrollments:
                receiver = enrollment.member.user
                notification_object = NotificationObject(
                    receiver=receiver, notification=notification)
                notification_object.save()
            # end for
        # end for
    # end if
# end def

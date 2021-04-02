from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import IndustryProject, IndustryProjectApplication
from courses.models import Course, Enrollment
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=IndustryProjectApplication)
def update_industry_project_application(sender, instance, created, **kwargs):
    industry_project = instance.industry_project
    partner = industry_project.partner

    if created:
        title = f'New application for Industry Project {industry_project.title}!'
        description = f'New application for Industry Project {industry_project.title} made by {instance.member}'
        notification_type = 'INDUSTRY_PROJECTS'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, industry_project=industry_project)
        notification.save()

        receiver = partner.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


@receiver(post_save, sender=IndustryProject)
def update_industry_project(sender, instance, created, **kwargs):
    industry_project = instance
    partner = instance.partner

    if created:
        title = f'New Industry Project {industry_project.title} available!'
        notification_type = 'INDUSTRY_PROJECTS'

        courses = Course.objects.filter(partner=partner)
        for course in courses:
            description = f'New Industry Project {industry_project.title} available by the instructor of {course}!'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, industry_project=industry_project)
            notification.save()
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

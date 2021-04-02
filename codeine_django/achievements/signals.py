from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MemberAchievement
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=MemberAchievement)
def update_member_achievement(sender, instance, created, **kwargs):
    achievement = instance.achievement
    receiver = instance.member.user

    if created:
        title = f'Congratulations! You met the requirements for a new achievement!'
        description = f'You have attained {achievement.title}!'
        notification_type = 'GENERAL'
        notification = Notification(
            title=title, description=description, notification_type=notification_type)
        notification.save()

        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def

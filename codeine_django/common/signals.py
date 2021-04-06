from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PaymentTransaction
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=PaymentTransaction)
def update_payment_transaction(sender, instance, created, **kwargs):

    if created:
        print('new payment transaction')
    else:
        title = f'Payment transaction updated!'
        description = f'Status changed to {instance.payment_status}'

        notification_type = 'PAYMENT'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, transaction=instance)
        notification.save()

        try:
            if instance.membership_subscription:
                receiver = instance.membership_subscription.member.user
            if instance.event_payment:
                receiver = instance.event_payment.event_application.member.user
            if instance.contribution_payment:
                receiver = instance.contribution_payment.made_by.user
            if instance.consultation_payment:
                receiver = instance.consultation_payment.consultation_application.member.user
            # end if

            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        except:
            print('error')
        # end try-except
    # end if-else
# end def

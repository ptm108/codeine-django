from django.db import models
import uuid

# Create your models here.


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('COURSE', 'Course'),
        ('ARTICLE', 'Article'),
        ('CODE_REVIEW', 'Code Review'),
        ('PAYMENT', 'Payment'),
        ('CONSULTATION', 'Consultation'),
        ('HELPDESK', 'Helpdesk'),
        ('INDUSTRY_PROJECTS', 'Industry Project'),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # enums
    notification_type = models.TextField(
        choices=NOTIFICATION_TYPES)

    # ref
    receiver = models.ForeignKey(
        'common.BaseUser', related_name='received_notifications', on_delete=models.SET_NULL, blank=True, null=True)
    sender = models.ForeignKey(
        'common.BaseUser', related_name='sent_notifications', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Notification {self.id}'
    # end def

    class Meta:
        ordering = ['timestamp']
    # end Meta
# end class

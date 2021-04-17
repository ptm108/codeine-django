from django.db import models
import uuid

# Create your models here.


def img_directory_path(instance, filename):
    return 'notifications/{1}'.format(instance.id, filename)
# end def


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('GENERAL', 'General'),
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
    photo = models.ImageField(
        upload_to=img_directory_path, max_length=100, blank=True, null=True, default=None)

    # enums
    notification_type = models.TextField(
        choices=NOTIFICATION_TYPES)

    # ref
    sender = models.ForeignKey(
        'common.BaseUser', related_name='sent_notifications', on_delete=models.SET_NULL, blank=True, null=True)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)
    article = models.ForeignKey(
        'community.Article', on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)
    code_review = models.ForeignKey(
        'community.CodeReview', on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)
    transaction = models.ForeignKey(
        'common.PaymentTransaction', on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)
    consultation_slot = models.ForeignKey(
        'consultations.ConsultationSlot', on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)
    ticket = models.ForeignKey('helpdesk.Ticket', on_delete=models.SET_NULL,
                               related_name="notifications", null=True, blank=True)
    industry_project = models.ForeignKey(
        'industry_projects.IndustryProject', on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)

    def __str__(self):
        return f'Notification: {self.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end Meta
# end class


class NotificationObject(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # ref
    receiver = models.ForeignKey(
        'common.BaseUser', related_name='received_notifications', on_delete=models.SET_NULL, blank=True, null=True)
    notification = models.ForeignKey(
        Notification, related_name='notification_objects', on_delete=models.CASCADE)

    def __str__(self):
        return f'Notification Object: {self.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end Meta
# end class

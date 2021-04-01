from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

import uuid

# Create your models here.


def img_directory_path(instance, filename):
    return 'user_{0}/helpdesk/{1}/{2}'.format(instance.base_user.id, instance.id, filename)
# end def


def file_directory_path(instance, filename):
    return 'user_{0}/helpdesk/{1}/{2}'.format(instance.ticket.base_user.id, instance.ticket.id, filename)
# end def


class Ticket(models.Model):
    TICKET_STATUSES = (
        ('OPEN', 'Open'),
        ('PENDING', 'Pending'),
        ('RESOLVED', 'Resolved')
    )

    TICKET_TYPES = (
        ('ACCOUNT', 'Account'),
        ('GENERAL', 'General'),
        ('TECHNICAL', 'Technical'),
        ('PAYMENT', 'Payments'),
        ('COURSE', 'Courses'),
        ('ARTICLE', 'Articles'),
        ('CODE_REVIEWS', 'Code Reviews'),
        ('INDUSTRY_PROJECT', 'Industry Projects'),
        ('CONSULTATION', 'Consultations'),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(
        upload_to=img_directory_path, max_length=100, blank=True, null=True, default=None)

    # enums
    ticket_status = models.TextField(choices=TICKET_STATUSES, default='OPEN')
    ticket_type = MultiSelectField(choices=TICKET_TYPES)

    # ref
    base_user = models.ForeignKey(
        'common.BaseUser', on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    transaction = models.ForeignKey(
        'common.PaymentTransaction', on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    article = models.ForeignKey(
        'community.Article', on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    industry_project = models.ForeignKey(
        'industry_projects.IndustryProject', on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    consultation_slot = models.ForeignKey(
        'consultations.ConsultationSlot', on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)
    code_review = models.ForeignKey(
        'community.CodeReview', on_delete=models.SET_NULL, related_name='tickets', null=True, blank=True)

    def __str__(self):
        return f'Ticket: {self.id}, Status: {self.ticket_status}, Type: {self.ticket_type}'
    # end def

    class Meta:
        ordering = ['-timestamp', 'ticket_status', 'ticket_type']
    # end class
# end class


class TicketMessage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to=file_directory_path, max_length=255, null=True, blank=True)

    # ref
    base_user = models.ForeignKey('common.BaseUser', on_delete=models.SET_NULL,
                                  related_name='ticket_messages', null=True, blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,
                               related_name='ticket_messages', null=True, blank=True)

    def __str__(self):
        return f'Ticket Message {self.id} for {self.ticket.id} from {self.base_user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end class
# end class

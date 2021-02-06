from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

import uuid

# Create your models here.
class Ticket(models.Model):
    TICKET_STATUSES = (
        ('OPEN', 'Open'),
        ('PENDING', 'Pending'),
        ('RESOLVED', 'Resolved')
    )

    TICKET_TYPES = (
        ('ARTICLE', 'Article'),
        ('QUERY', 'Query'),
        ('ENROLLMENT', 'Enrollment')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    # enums
    ticket_status = models.TextField(choices=TICKET_STATUSES, default='OPEN')
    ticket_type = MultiSelectField(choices=TICKET_TYPES)

    # ref
    base_user = models.ForeignKey('common.BaseUser', on_delete=models.SET_NULL, related_name='cp_consultation_slots', null=True, blank=True)

    def __str__(self):
        return f'Ticket: {self.id}, Status: {self.ticket_status}, Type: {self.ticket_type}'
    # end def

    class Meta:
        ordering = ['timestamp', 'ticket_status', 'ticket_type']
    #end class
# end class


class TicketMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    # ref
    base_user = models.ForeignKey('common.BaseUser', on_delete=models.SET_NULL, related_name='ticket_messages', null=True, blank=True)
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.SET_NULL, related_name='ticket_messages', null=True, blank=True)

    def __str__(self):
        return f'Ticket Message {self.id} for {self.ticket.id} from {self.base_user.id}'
    # end def

    class Meta:
        ordering = ['timestamp']
    #end class
# end class

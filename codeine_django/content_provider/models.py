from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

import uuid

# Create your models here.
class ConsultationSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_link = models.TextField(default='')
    is_confirmed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    # ref
    content_provider = models.ForeignKey('common.ContentProvider', on_delete=models.SET_NULL, related_name='consultation_slots', null=True)
    member = models.ForeignKey('common.Member', on_delete=models.SET_NULL, related_name='consultation_slots', null=True)

    def __str__(self):
        return f'Consultation slot on {self.start_date} at {self.start_time} to {self.end_date} {self.end_time}'
    # end def

    class Meta:
        ordering = ['start_date', 'start_time', 'end_date', 'end_time']
    #end class
# end class


class PaymentTransaction(models.Model):
    PAYMENT_STATUSES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('REFUNDED', 'Refunded'),
        ('FAILED', 'Failed')
    )

    PAYMENT_TYPES = (
        ('VISA', 'Visa'),
        ('MASTER', 'Mastercard'),
        ('AMEX', 'American Express')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    # enums
    payment_status = MultiSelectField(choices=PAYMENT_STATUSES)
    payment_type = MultiSelectField(choices=PAYMENT_TYPES)

    # ref
    consultation_slot = models.OneToOneField('ConsultationSlot', on_delete=models.DO_NOTHING, related_name="transaction", null=True)
    enrollment = models.OneToOneField('courses.Enrollment', on_delete=models.DO_NOTHING, related_name="transaction", null=True)

    def __str__(self):
        return f'Payment of {self.payment_amount} using {self.payment_type}, status: {self.payment_status}'
    # end def

    class Meta:
        ordering = ['timestamp']
    #end class
# end class

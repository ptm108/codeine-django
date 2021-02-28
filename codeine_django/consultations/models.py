from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

import uuid

# Create your models here.


class ConsultationSlot(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # start_date = models.DateField()
    # end_date = models.DateField()
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_link = models.TextField(default='')
    # is_confirmed = models.BooleanField(default=False)
    # is_rejected = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    price_per_pax = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0)
    max_members = models.IntegerField()
    # r_rule = models.TextField(null=True, blank=True)
    # is_all_day = models.BooleanField(default=False)

    # ref
    partner = models.ForeignKey('common.Partner', on_delete=models.SET_NULL,
                                related_name='consultation_slots', null=True, blank=True)
    # member = models.ForeignKey('common.Member', on_delete=models.SET_NULL, related_name='consultation_slots', null=True, blank=True)

    def __str__(self):
        return f'Consultation slot: {self.id}'
    # end def

    class Meta:
        ordering = ['start_time', 'end_time']
        # ordering = ['start_date', 'start_time', 'end_date', 'end_time']
    # end class
# end class


class ConsultationApplication(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    is_cancelled = models.BooleanField(default=False)  # cancelled by member
    is_rejected = models.BooleanField(default=False)  # rejected by partner

    # ref
    member = models.ForeignKey('common.Member', on_delete=models.SET_NULL,
                               related_name='consultation_applications', null=True, blank=True)
    consultation_slot = models.ForeignKey(
        ConsultationSlot, on_delete=models.SET_NULL, related_name='consultation_applications', null=True, blank=True)

    def __str__(self):
        return f'Application for {self.consultation_slot}'
    # end def
# end class


class ConsultationPayment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payment_transaction = models.OneToOneField(
        'common.PaymentTransaction', on_delete=models.CASCADE)

    # ref
    consultation_application = models.ForeignKey(
        ConsultationApplication, on_delete=models.SET_NULL, related_name='consultation_payments', null=True, blank=True)

    def __str__(self):
        return f'{self.payment_transaction} for {self.consultation_application}'
    # end def
# end class

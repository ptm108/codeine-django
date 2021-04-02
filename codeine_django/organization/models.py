from django.db import models

import uuid

# Create your models here.


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_link = models.TextField(default='')
    is_cancelled = models.BooleanField(default=False)
    price_per_pax = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    max_members = models.IntegerField()

    # ref
    organization = models.ForeignKey('common.Organization', on_delete=models.SET_NULL, related_name='events', null=True, blank=True)

    def __str__(self):
        return f'Event: {self.id}'
    # end def

    class Meta:
        ordering = ['start_time', 'end_time']
    # end class
# end class


class EventApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    is_cancelled = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    # ref
    member = models.ForeignKey('common.Member', on_delete=models.SET_NULL, related_name='event_applications', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, related_name='event_applications', null=True, blank=True)

    def __str__(self):
        return f'Application for {self.event}'
    # end def
# end class


class EventPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payment_transaction = models.OneToOneField('common.PaymentTransaction', on_delete=models.CASCADE, related_name="event_payment")

    # ref
    event_application = models.ForeignKey(EventApplication, on_delete=models.SET_NULL, related_name='event_payments', null=True, blank=True)

    def __str__(self):
        return f'{self.payment_transaction}'
    # end def
# end class


class ContributionPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payment_transaction = models.OneToOneField('common.PaymentTransaction', on_delete=models.CASCADE, related_name="contribution_payment")
    timestamp = models.DateTimeField(auto_now_add=True)
    # month_duration = models.PositiveSmallIntegerField(default=1)
    # expiry_date = models.DateTimeField()

    # ref
    organization = models.ForeignKey('common.Organization', on_delete=models.SET_NULL, related_name='contribution_payments', null=True, blank=True)
    made_by = models.ForeignKey('common.Partner', on_delete=models.SET_NULL, related_name='contributions_made', null=True, blank=True)

    def __str__(self):
        return f'{self.payment_transaction}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end Meta
# end class

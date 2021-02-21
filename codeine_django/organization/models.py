from django.db import models

import uuid

# Create your models here.
class EventPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payment_transaction = models.OneToOneField('common.PaymentTransaction', on_delete=models.CASCADE)
    
    # ref
    organization = models.ForeignKey('common.Organization', on_delete=models.SET_NULL, related_name='contribution_payments', null=True, blank=True)

    def __str__(self):
        return f'{self.payment_transaction}'
    # end def
# end class

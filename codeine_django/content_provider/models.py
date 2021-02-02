from django.db import models
from django.utils import timezone
from common.models import ContentProvider, Member

import uuid

# Create your models here.
class ConsultationSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_link = models.TextField(default='')
    is_cancelled = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    content_provider = models.ForeignKey(ContentProvider, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Consultation slot on {self.start_date} at {self.start_time} to {self.end_date} {self.end_time}'
    # end def

    class Meta:
        ordering = ['start_date', 'start_time', 'end_date', 'end_time']
    #end class
# end class

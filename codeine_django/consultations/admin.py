from django.contrib import admin

from .models import ConsultationSlot, PaymentTransaction


class ConsultationSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'meeting_link', 'is_confirmed', 'is_rejected', 'partner', 'member')
# end class


class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'payment_amount', 'payment_status', 'payment_type', 'consultation_slot', 'enrollment')
# end class

admin.site.register(ConsultationSlot, ConsultationSlotAdmin)
admin.site.register(PaymentTransaction, PaymentTransactionAdmin)

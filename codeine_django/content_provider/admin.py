from django.contrib import admin

from .models import ConsultationSlot, PaymentTransaction


# Register your models here.
class ConsultationSlotInline(admin.StackedInline):
    model = ConsultationSlot
    can_delete = False
    verbose_name_plural = 'Consultation Slots'
# end class


class PaymentTransactionInline(admin.StackedInline):
    model = PaymentTransaction
    can_delete = False
    verbose_name_plural = 'Payment Transactions'
# end class


class ConsultationSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'meeting_link', 'is_confirmed', 'is_rejected', 'content_provider', 'member')
    # list_display = ('id', 'start_date', 'start_time', 'end_date', 'end_time', 'meeting_link', 'is_confirmed', 'is_rejected', 'content_provider', 'member')
# end class


class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'payment_amount', 'payment_status', 'payment_type', 'consultation_slot', 'enrollment')
# end class

admin.site.register(ConsultationSlot, ConsultationSlotAdmin)
admin.site.register(PaymentTransaction, PaymentTransactionAdmin)

from django.contrib import admin

from .models import ConsultationSlot, ConsultationApplication, ConsultationPayment


class ConsultationSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'meeting_link', 'is_cancelled', 'price_per_pax', 'max_members', 'partner')
    # list_display = ('id', 'title', 'start_time', 'end_time', 'meeting_link', 'is_confirmed', 'is_rejected', 'partner', 'member')
# end class


class ConsultationApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_cancelled', 'is_rejected', 'member', 'consultation_slot')
# end class


class ConsultationPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_transaction', 'consultation_application')
# end class


admin.site.register(ConsultationSlot, ConsultationSlotAdmin)
admin.site.register(ConsultationApplication, ConsultationApplicationAdmin)
admin.site.register(ConsultationPayment, ConsultationPaymentAdmin)

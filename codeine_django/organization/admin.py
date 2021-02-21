from django.contrib import admin

from .models import Event, EventApplication, EventPayment, ContributionPayment

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'meeting_link', 'is_cancelled', 'price_per_pax', 'max_members', 'organization')
# end class


class EventApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_cancelled', 'is_rejected', 'member', 'event')
# end class


class EventPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_transaction', 'event_application')
# end class


class ContributionPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_transaction', 'organization')
# end class

admin.site.register(Event, EventAdmin)
admin.site.register(EventApplication, EventApplicationAdmin)
admin.site.register(EventPayment, EventPaymentAdmin)
admin.site.register(ContributionPayment, ContributionPaymentAdmin)

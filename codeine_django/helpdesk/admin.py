from django.contrib import admin

from .models import Ticket, TicketMessage

# Register your models here.


class TicketInline(admin.StackedInline):
    model = Ticket
    can_delete = False
    verbose_name_plural = 'Tickets'
# end class


class TicketMessageInline(admin.StackedInline):
    model = TicketMessage
    can_delete = False
    verbose_name_plural = 'Ticket Messages'
# end class


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'timestamp', 'photo', 'ticket_status', 'ticket_type',
                    'base_user', 'transaction', 'course', 'article', 'industry_project', 'consultation_slot')
# end class


class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'timestamp', 'base_user', 'ticket')
# end class


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketMessage, TicketMessageAdmin)

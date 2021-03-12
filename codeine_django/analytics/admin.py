from django.contrib import admin

from .models import EventLog
class EventLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'payload',
        'timestamp',
    )
# end class

admin.site.register(EventLog, EventLogAdmin)

from django.contrib import admin

from .models import EventLog
class EventLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'payload',
        'user',
        'course',
        'course_material',
        'quiz',
        'industry_project',
    )
# end class

admin.site.register(EventLog, EventLogAdmin)

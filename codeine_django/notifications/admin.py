from django.contrib import admin
from .models import Notification
# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'timestamp',
                    'is_read', 'notification_type', 'receiver', 'sender')
# end class


admin.site.register(Notification, NotificationAdmin)

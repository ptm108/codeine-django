from django.contrib import admin
from .models import Notification, NotificationObject
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'timestamp',
                    'notification_type', 'sender')
# end class


class NotificationObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'receiver')
# end class


admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationObject, NotificationObjectAdmin)

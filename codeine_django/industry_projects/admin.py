from django.contrib import admin

from .models import IndustryProject, IndustryProjectApplication


class IndustryProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_available',
        'is_completed',
    )
# end class


class IndustryProjectApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_accepted',
        'member',
    )
# end class


admin.site.register(IndustryProject, IndustryProjectAdmin)
admin.site.register(IndustryProjectApplication, IndustryProjectApplicationAdmin)

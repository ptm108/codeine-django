from django.contrib import admin

from .models import Achievement, AchievementRequirement
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_deleted',
        'timestamp',
    )
# end class


class AchievementRequirementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category', 
        'coding_languages',
        'experience_point',
    )
# end class

admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchievementRequirement, AchievementRequirementAdmin)

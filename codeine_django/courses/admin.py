from django.contrib import admin

from .models import Course, Chapter, CourseMaterial, Video, CourseFile, Quiz


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'is_available',
        'is_deleted',
        'content_provider',
        'rating',
        'exp_points',
    )
# end class


class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'overview',
        'order',
        'course',
        'timestamp',
    )
# end class


class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'material_type',
        'order',
        'chapter',
        'timestamp',
    )
# end class


class CourseFileAdmin(admin.ModelAdmin):
    list_display = (
        'zip_file',
        'google_drive_url',
        'course_material',
    )
# end class


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'video_url',
    )
# end class


admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)
admin.site.register(CourseFile, CourseFileAdmin)
admin.site.register(Video, VideoAdmin)

from django.contrib import admin

from .models import Course, Chapter, CourseMaterial, Video, CourseFile, Quiz, Question, ShortAnswer, MCQ, MRQ, Enrollment


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'is_available',
        'is_deleted',
        'partner',
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


class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'passing_marks',
        'instructions',
        'course_material',
        'course',
    )
# end class


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'subtitle',
        'order',
        'quiz',
    )
# end class


class ShortAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'marks',
        'keywords',
    )
# end class


class MCQAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'marks',
        'options',
        'correct_answer',
    )
# end class


class MRQAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'marks',
        'options',
        'correct_answer',
    )
# end class


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'date_created',
        'progress',
        'course',
        'member',
    )
# end class


admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)
admin.site.register(CourseFile, CourseFileAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ShortAnswer, ShortAnswerAdmin)
admin.site.register(MCQ, MCQAdmin)
admin.site.register(MRQ, MRQAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)

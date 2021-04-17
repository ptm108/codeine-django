from django.contrib import admin

from .models import (
    Course,
    Chapter,
    CourseMaterial,
    Video,
    CourseFile,
    Quiz,
    Question,
    QuestionBank,
    QuestionGroup,
    ShortAnswer,
    MCQ,
    MRQ,
    Enrollment,
    QuizResult,
    QuizAnswer,
    CourseReview,
    CourseComment,
    CourseCommentEngagement
)


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'is_available',
        'is_deleted',
        'partner',
        'rating',
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
        'image',
        'question_bank',
    )
# end class


class QuestionBankAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'label',
        'course',
    )
# end class


class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'quiz',
        'question_bank',
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


class QuizResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date_created',
        'score',
        'passed',
        'submitted',
        'member',
        'quiz',
    )
# end class


class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'quiz_result',
        'question',
        'response',
        'responses',
    )
# end class


class CourseReviewAdmin(admin.ModelAdmin):
    list_display = (
        'rating',
        'description',
        'timestamp',
        'course',
        'member'
    )
# end class


class CourseCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'comment',
        'timestamp',
        'pinned',
        'course_material',
        'user',
        'reply_to',
    )
# end class


class CourseCommentEngagementAdmin(admin.ModelAdmin):
    list_display = (
        'comment',
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
admin.site.register(QuestionBank, QuestionBankAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(ShortAnswer, ShortAnswerAdmin)
admin.site.register(MCQ, MCQAdmin)
admin.site.register(MRQ, MRQAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(QuizAnswer, QuizAnswerAdmin)
admin.site.register(CourseReview, CourseReviewAdmin)
admin.site.register(CourseComment, CourseCommentAdmin)
admin.site.register(CourseCommentEngagement, CourseCommentEngagementAdmin)

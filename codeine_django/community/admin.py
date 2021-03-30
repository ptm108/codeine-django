from django.contrib import admin

from .models import Article, ArticleComment, ArticleEngagement, CodeReview, CodeReviewComment, CodeReviewEngagement

# Register your models here.


class ArticleInline(admin.StackedInline):
    model = Article
    can_delete = False
    verbose_name_plural = 'Articles'
# end class


class ArticleCommentInline(admin.StackedInline):
    model = ArticleComment
    can_delete = False
    verbose_name_plural = 'Article Comments'
# end class


class ArticleEngagementInline(admin.StackedInline):
    model = ArticleEngagement
    can_delete = False
    verbose_name_plural = 'Article Engagements'
# end class


class CodeReviewInline(admin.StackedInline):
    model = CodeReview
    can_delete = False
    verbose_name_plural = 'Code Reviews'
# end class


class CodeReviewCommentInline(admin.StackedInline):
    model = CodeReviewComment
    can_delete = False
    verbose_name_plural = 'Code Review Comments'
# end class


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'date_created',
                    'date_edited', 'coding_languages', 'languages', 'categories', 'is_published', 'is_activated', 'user')
# end class


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'timestamp', 'user', 'article')
# end class


class ArticleEngagementAdmin(admin.ModelAdmin):
    # list_display = ('id', 'like', 'timestamp', 'user', 'article')
    list_display = ('id', 'timestamp', 'user', 'article')
# end class


class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'timestamp',
                    'coding_languages', 'categories', 'user')
# end class


class CodeReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'timestamp', 'user',
                    'code_review', 'parent_comment')

    # list_display = ('id', 'highlighted_code', 'comment',
    #                 'timestamp', 'user', 'code_review', 'parent_comment', 'start_index', 'end_index')
# end class


class CodeReviewEngagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'user', 'code_review')
    # list_display = ('id', 'like', 'timestamp', 'user', 'code_review')
# end class


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
admin.site.register(ArticleEngagement, ArticleEngagementAdmin)
admin.site.register(CodeReview, CodeReviewAdmin)
admin.site.register(CodeReviewComment, CodeReviewCommentAdmin)
admin.site.register(CodeReviewEngagement, CodeReviewEngagementAdmin)

from django.contrib import admin

from .models import Article, ArticleComment, Engagement, CodeReview, CodeReviewComment

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

class EngagementInline(admin.StackedInline):
    model = Engagement
    can_delete = False
    verbose_name_plural = 'Engagements'
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
    list_display = ('id', 'title', 'content', 'date_created', 'date_edited', 'is_published', 'is_activated', 'member')
# end class

class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'timestamp', 'user', 'article')
# end class

class EngagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'like', 'timestamp', 'member', 'article')
# end class

class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'timestamp', 'coding_languages', 'categories', 'member')
# end class

class CodeReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'highlighted_code', 'comment', 'timestamp', 'user', 'code_review', 'parent_comment')
# end class

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
admin.site.register(Engagement, EngagementAdmin)
admin.site.register(CodeReview, CodeReviewAdmin)
admin.site.register(CodeReviewComment, CodeReviewCommentAdmin)

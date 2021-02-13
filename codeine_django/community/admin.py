from django.contrib import admin

from .models import Article, ArticleComment

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


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'date_created', 'date_edited', 'is_published', 'is_activated', 'member')
# end class


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'timestamp', 'member', 'article')
# end class

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)

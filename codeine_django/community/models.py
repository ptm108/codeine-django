from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

import uuid

# Create your models here.
class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    category = models.JSONField()
    is_published = models.BooleanField(default=True)
    is_activated = models.BooleanField(default=True)

    # ref
    member = models.ForeignKey('common.Member', on_delete=models.CASCADE, related_name='articles', null=False, blank=True)

    def __str__(self):
        return f'Article: {self.id}, Title: {self.title}'
    # end def

    class Meta:
        ordering = ['-date_edited']
    #end class
# end class

class ArticleComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    comment = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    # ref
    base_user = models.ForeignKey('common.BaseUser', on_delete=models.SET_NULL, related_name='article_comments')
    article = models.ForeignKey('community.Article', on_delete=models.CASCADE, related_name='article_comments')

    def __str__(self):
        return f'Article comment {self.id} for {self.article.id} from {self.base_user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    #end class
# end class

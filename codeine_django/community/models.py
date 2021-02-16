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
    member = models.ForeignKey('common.Member', on_delete=models.CASCADE, related_name='articles')

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
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='article_comments')
    article = models.ForeignKey('community.Article', on_delete=models.CASCADE, related_name='article_comments')
    parent_comment = models.ForeignKey('community.ArticleComment', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f'Article comment {self.id} for {self.article.id} from {self.user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    #end class
# end class


class Engagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    like = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ref
    member = models.ForeignKey('common.Member', on_delete=models.CASCADE, related_name='engagements')
    article = models.ForeignKey('community.Article', on_delete=models.CASCADE, related_name='engagements')

    def __str__(self):
        return f'Engagement {self.id} for {self.article.id} from {self.member.user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    #end class
#end class

class CodeReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    code = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    coding_languages = models.JSONField()
    categories = models.JSONField()

    # ref
    member = models.ForeignKey('common.Member', on_delete=models.CASCADE, related_name='code_reviews')

    def __str__(self):
        return f'Code Review {self.id} request from {self.member.user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    #end class
#end class

class CodeReviewComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    highlighted_code = models.TextField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ref
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='code_review_comments')
    code_review = models.ForeignKey('community.CodeReview', on_delete=models.CASCADE, related_name='code_review_comments')
    parent_comment = models.ForeignKey('community.CodeReviewComment', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f'Code Review Comment {self.id} for Code Review {self.code_review.id} from {self.user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    #end class
#end class

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

from multiselectfield import MultiSelectField
import json
import uuid


def article_directory_path(instance, filename):
    return 'article_{0}/{1}'.format(instance.id, filename)
# end def


# Create your models here.
class Article(models.Model):
    CODING_LANGUAGES = (
        ('PY', 'Python'),
        ('JAVA', 'Java'),
        ('JS', 'Javascript'),
        ('CPP', 'C++'),
        ('CS', 'C#'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('RUBY', 'Ruby'),
    )

    LANGUAGES = (
        ('ENG', 'English'),
        ('MAN', 'Mandarin'),
        ('FRE', 'French'),
    )

    CATEGORIES = (
        ('SEC', 'Security'),
        ('DB', 'Database Administration'),
        ('FE', 'Frontend'),
        ('BE', 'Backend'),
        ('UI', 'UI/UX'),
        ('ML', 'Machine Learning'),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(
        upload_to=article_directory_path, max_length=100, blank=True, null=True, default=None)

    # availability
    is_published = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)

    # enums
    coding_languages = MultiSelectField(choices=CODING_LANGUAGES)
    languages = MultiSelectField(choices=LANGUAGES)
    categories = MultiSelectField(choices=CATEGORIES)

    # ref
    # member = models.ForeignKey(
    #     'common.Member', on_delete=models.CASCADE, related_name='articles')
    user = models.ForeignKey(
        'common.BaseUser', on_delete=models.CASCADE, related_name='articles', null=True, default=None)

    def __str__(self):
        return f'Article: {self.id}, Title: {self.title}'
    # end def

    class Meta:
        ordering = ['date_edited']
    # end class
# end class


class ArticleComment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    display_id = models.PositiveIntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)
    pinned = models.BooleanField(default=False)

    # ref
    user = models.ForeignKey(
        'common.BaseUser', on_delete=models.CASCADE, related_name='article_comments')
    article = models.ForeignKey(
        'community.Article', on_delete=models.CASCADE, related_name='article_comments')
    reply_to = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f'Article comment {self.id} for {self.article.id} from {self.user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end class
# end class


class ArticleEngagement(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # like = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ref
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='article_engagements', null=True, default=None)
    article = models.ForeignKey('community.Article', on_delete=models.CASCADE, related_name='engagements')

    def __str__(self):
        return f'Article Engagement {self.id} for Article {self.article.id} from {self.user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end class
# end class


class ArticleCommentEngagement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    # ref
    comment = models.ForeignKey('ArticleComment', on_delete=models.CASCADE, related_name='engagements')
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='+')
# end class


class CodeReview(models.Model):
    CODING_LANGUAGES = (
        ('PY', 'Python'),
        ('JAVA', 'Java'),
        ('JS', 'Javascript'),
        ('CPP', 'C++'),
        ('CS', 'C#'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('RUBY', 'Ruby'),
    )

    LANGUAGES = (
        ('ENG', 'English'),
        ('MAN', 'Mandarin'),
        ('FRE', 'French'),
    )

    CATEGORIES = (
        ('SEC', 'Security'),
        ('DB', 'Database Administration'),
        ('FE', 'Frontend'),
        ('BE', 'Backend'),
        ('UI', 'UI/UX'),
        ('ML', 'Machine Learning'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    code = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # enums
    coding_languages = MultiSelectField(choices=CODING_LANGUAGES)
    languages = MultiSelectField(choices=LANGUAGES)
    categories = MultiSelectField(choices=CATEGORIES)

    # ref
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='code_reviews', null=True, default=None)

    def __str__(self):
        return f'Code Review {self.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end class
# end class


class CodeReviewComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)

    code_line_index = models.PositiveIntegerField()

    # ref
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='code_review_comments')
    code_review = models.ForeignKey('community.CodeReview', on_delete=models.CASCADE, related_name='code_review_comments')
    parent_comment = models.ForeignKey('community.CodeReviewComment', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f'Code Review Comment {self.id} for Code Review {self.code_review.id} from {self.user.id}'
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end class
# end class


class CodeReviewEngagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # ref
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='code_review_engagements', null=True, default=None)
    code_review = models.ForeignKey('community.CodeReview', on_delete=models.CASCADE, related_name='engagements')

    def __str__(self):
        return f'Code Review Engagement {self.id} for Code Review {self.code_review.id} '
    # end def

    class Meta:
        ordering = ['-timestamp']
    # end class
# end class


class CodeReviewCommentEngagement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    # ref
    comment = models.ForeignKey('CodeReviewComment', on_delete=models.CASCADE, related_name='engagements')
    user = models.ForeignKey('common.BaseUser', on_delete=models.CASCADE, related_name='+')
# end class

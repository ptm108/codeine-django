from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

import uuid


def image_directory_path(instance, filename):
    return 'course_{0}/image_{1}'.format(instance.id, filename)
# end def


def zipfile_directory_path(instance, filename):
    return 'course_{0}/chapter_{1}/{2}'.format(instance.course_material.chapter.course.id, instance.course_material.chapter.id, filename)
# end def


def validate_rating(value):
    if (value < 1 or value > 5):
        raise ValidationError(_('%(value)s is not a valid rating'), params={'value': value})
    # end if
# end def


class Course(models.Model):
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
    learning_objectives = models.JSONField()  # list of objectives
    requirements = models.JSONField()  # list of requirements
    description = models.TextField()
    introduction_video_url = models.CharField(max_length=255, null=True, blank=True, default=None)
    github_repo = models.CharField(max_length=255, null=True, blank=True, default=None)
    thumbnail = models.ImageField(upload_to=image_directory_path, max_length=100, null=True, default=None)
    views = models.PositiveIntegerField(default=0)

    # enums
    coding_languages = MultiSelectField(choices=CODING_LANGUAGES)
    languages = MultiSelectField(choices=LANGUAGES)
    categories = MultiSelectField(choices=CATEGORIES)

    # publishing details
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, default=None, blank=True)

    # availability
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # price in cents
    price = models.PositiveIntegerField()

    # cert in html
    certificate = models.TextField(null=True, default=None, blank=True)

    # provider ref
    partner = models.ForeignKey('common.Partner', on_delete=models.SET_NULL, related_name='courses', null=True)

    # rating, updated by trigger
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    # experience points - set by content_provider
    exp_points = models.PositiveIntegerField(default=0)
# end class


class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(null=True, default='')
    order = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='chapters')

    class Meta:
        ordering = ['order']
    # end Meta
# end class


class CourseMaterial(models.Model):
    class MaterialType(models.TextChoices):  # to extend
        FILE = 'FILE', _('File')
        VIDEO = 'VIDEO', _('Video')
        QUIZ = 'QUIZ', _('Quiz')
    # end class

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, default='', blank=True)
    material_type = models.CharField(max_length=255, choices=MaterialType.choices)
    order = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='course_materials', null=True, blank=True)

    class Meta:
        ordering = ['order']
    # end Meta
# end class


class CourseFile(models.Model):
    course_material = models.OneToOneField('CourseMaterial', on_delete=models.CASCADE, related_name='course_file')
    zip_file = models.FileField(upload_to=zipfile_directory_path, max_length=255, null=True, blank=True)
    google_drive_url = models.TextField(null=True, default='', blank=True)
# end class


class Video(models.Model):
    course_material = models.OneToOneField('CourseMaterial', on_delete=models.CASCADE, related_name='video')
    video_url = models.URLField()
# end class


class Enrollment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2)

    # ref for course
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, related_name='enrollments')

    # ref for member
    member = models.ForeignKey('common.Member', on_delete=models.CASCADE, related_name='enrollments')
# end class


class CourseReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    rating = models.PositiveSmallIntegerField(validators=[validate_rating])
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # ref for course
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, related_name='course_reviews')

    # ref for member
    member = models.ForeignKey('common.Member', on_delete=models.CASCADE, related_name='+')
# end class


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    passing_marks = models.PositiveIntegerField(default=None, null=True, blank=True)

    # extends course material
    course_material = models.OneToOneField('CourseMaterial', on_delete=models.CASCADE)

    # either mapped to chapter or course
    course = models.OneToOneField('Course',  on_delete=models.CASCADE, related_name='quiz', null=True, blank=True)
# end class


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField()
    subtitle = models.TextField(null=True, default='', blank=True)

    # ref to Assessment
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
# end class


class ShortAnswer(models.Model):
    question = models.OneToOneField('Question', on_delete=models.CASCADE, null=True, blank=True)
    marks = models.PositiveIntegerField(default=1)
    keywords = models.JSONField()
# end class


class MCQ(models.Model):
    question = models.OneToOneField('Question', on_delete=models.CASCADE, null=True, blank=True)
    marks = models.PositiveIntegerField(default=1)
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255)
# end class


class MRQ(models.Model):
    question = models.OneToOneField('Question', on_delete=models.CASCADE, null=True, blank=True)
    marks = models.PositiveIntegerField(default=1)
    options = models.JSONField()
    correct_answer = models.JSONField()
# end class


class QuizResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    total_marks = models.PositiveIntegerField()
    passed = models.BooleanField(default=False)

    # member who took assessment
    member = models.ForeignKey('common.Member', on_delete=models.CASCADE, related_name='quiz_results')

    # assessment ref
    quiz = models.ForeignKey('Quiz', on_delete=models.SET_NULL, null=True, related_name='quiz_results')
# end class


class QuizAnswer(models.Model):
    # parent assessment result
    quiz_result = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='quiz_answers')

    # ref to question
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, related_name='quiz_answers')

    response = models.TextField(null=True, blank=True)
    responses = models.JSONField(null=True, blank=True)
# end class

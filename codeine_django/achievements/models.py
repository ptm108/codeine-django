from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

import uuid


def image_directory_path(instance, filename):
    return 'course_{0}/image_{1}'.format(instance.id, filename)
# end def

class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    badge = models.ImageField(upload_to=image_directory_path, max_length=100, null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

# end class

class AchievementRequirement(models.Model):
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

    CATEGORIES = (
        ('SEC', 'Security'),
        ('DB', 'Database Administration'),
        ('FE', 'Frontend'),
        ('BE', 'Backend'),
        ('UI', 'UI/UX'),
        ('ML', 'Machine Learning'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    category = choices=CODING_LANGUAGES
    coding_languages = choices=CATEGORIES
    experience_point = models.PositiveIntegerField()

    achievement = models.ForeignKey('Achievement', on_delete=models.CASCADE, related_name='achievement_requirements')
# end class
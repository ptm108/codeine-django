from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

import uuid


class IndustryProject(models.Model):
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
    description = models.CharField(max_length=255)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    application_deadline = models.DateField(null=True, default=None)
    is_available = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    categories = MultiSelectField(choices=CATEGORIES, null=True, default=None)

    # provider ref
    partner = models.ForeignKey('common.Partner', on_delete=models.SET_NULL, related_name='industry_projects', null=True)

# end class


class IndustryProjectApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    industry_project = models.ForeignKey('IndustryProject', on_delete=models.CASCADE, related_name='industry_project_applications')

    # member ref
    member = models.ForeignKey('common.Member', on_delete=models.SET_NULL, related_name='industry_project_applications', null=True)

# end class

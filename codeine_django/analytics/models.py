from django.db import models

import uuid


class EventLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payload = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('common.BaseUser', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, default=None)
    course_material = models.ForeignKey('courses.CourseMaterial', on_delete=models.CASCADE, null=True, blank=True, default=None)
    quiz = models.ForeignKey('course.Quiz', on_delete=models.CASCADE, null=True, blank=True, default=None)
    industry_project = models.ForeignKey('industry-projects.IndustryProject', on_delete=models.CASCADE, null=True, blank=True, default=None)
# end class

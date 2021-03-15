from django.db import models

import uuid


class EventLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    # payloads:
    # 1. "course view", course
    # 2. "continue course", course, user
    # 3. "stop course", course, user,
    # 4. "continue course material", course material, user
    # 5. "stop course material", course material, user
    # 6. "start assessment", quiz, user
    # 7. "stop assessment", quiz, user
    # 8. "search course", search string, user
    # 9. "search industry project", search string, user
    # 10. "view industry project", industry project, user
    payload = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('common.BaseUser', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, default=None)
    course_material = models.ForeignKey('courses.CourseMaterial', on_delete=models.CASCADE, null=True, blank=True, default=None)
    quiz = models.ForeignKey('courses.Quiz', on_delete=models.CASCADE, null=True, blank=True, default=None)
    industry_project = models.ForeignKey('industry_projects.IndustryProject', on_delete=models.CASCADE, null=True, blank=True, default=None)
    duration = models.PositiveBigIntegerField(null=True, blank=True, default=None)

    search_string = models.CharField(max_length=255)

    class Meta:
        ordering = ['-timestamp']
    # end Meta
# end class

from django.urls import path

from . import views_course_comments

urlpatterns = [
    # course material comment views
    path('/<slug:comment_id>', views_course_comments.single_course_comment_view, name='Get/Delete/Update Comment'),
]

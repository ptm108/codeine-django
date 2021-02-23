from django.urls import path

from . import views_course_comments

urlpatterns = [
    # course material comment views
    path('/<slug:comment_id>', views_course_comments.single_course_comment_view, name='Get/Delete/Update Comment'),
    path('/<slug:comment_id>/pin', views_course_comments.pin_comment_view, name='Pin a comment'),
    path('/<slug:comment_id>/unpin', views_course_comments.unpin_comment_view, name='Unpin a comment'),
    path('/<slug:comment_id>/engagements', views_course_comments.comment_engagement_view, name='Like/Unlike comment'),
]

from django.urls import path

from . import views_course_materials, views_course_comments

urlpatterns = [
    # course material views
    path('/<slug:material_id>/files', views_course_materials.update_file_view, name='Update material (file)'),
    path('/<slug:material_id>/videos', views_course_materials.update_video_view, name='Update material (video)'),
    path('/<slug:material_id>/quizzes', views_course_materials.update_quiz_view, name='Update material (quiz)'),
    path('/<slug:material_id>', views_course_materials.single_material_view, name='Get/Delete Material'),

    # course material comment views
    path('/<slug:material_id>/course-comments', views_course_comments.course_comments_view, name='Create/Get all comments under material'),
]

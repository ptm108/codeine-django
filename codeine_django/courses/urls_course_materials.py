from django.urls import path

from . import views_course_materials

urlpatterns = [
    # course material views
    path('/files/<slug:material_id>', views_course_materials.update_file_view, name='Create material (file)'),
    # path('/<slug:chapter_id>/videos', views_course_materials.video_views, name='Create material (video)'),
]

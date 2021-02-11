from django.urls import path

from . import views_course_materials

urlpatterns = [
    # course material views
    path('/files/<slug:material_id>', views_course_materials.update_file_view, name='Update material (file)'),
    path('/videos/<slug:material_id>', views_course_materials.update_video_view, name='Update material (video)'),
]

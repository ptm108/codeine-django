from django.urls import path

from . import views_course_materials

urlpatterns = [
    # course material views
    path('/<slug:material_id>/files', views_course_materials.update_file_view, name='Update material (file)'),
    path('/<slug:material_id>/videos', views_course_materials.update_video_view, name='Update material (video)'),
    path('/<slug:material_id>', views_course_materials.delete_material_view, name='Delete Material'),
]

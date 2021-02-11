from django.urls import path

from . import views_course_materials

urlpatterns = [
    # course material views
    path('/<slug:chapter_id>/files', views_course_materials.file_views, name='Create material (file)'),
    path('/<slug:chapter_id>/videos', views_course_materials.video_views, name='Create material (video)'),
    path('/<slug:chapter_id>/orderMaterials', views_course_materials.order_material_view, name='Order course materials by id'),
]

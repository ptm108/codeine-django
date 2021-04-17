from django.urls import path

from . import views_member_public

urlpatterns = [
    # members views
    path('<slug:pk>/profile', views_member_public.public_member_course_view, name='Get member public profile'),
    path('<slug:unique_id>/check-unique-id', views_member_public.check_unique_id_view, name='Get member public profile'),
]

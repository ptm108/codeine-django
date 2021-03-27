from django.urls import path

from . import views_member_public

urlpatterns = [
    # members views
    path('<slug:pk>/profile', views_member_public.public_member_course_view, name='Get member public profile'),
]

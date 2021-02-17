from django.urls import path

from . import views_protected_courses
urlpatterns = [
    # order views
    path('', views_protected_courses.course_view, name='Get all/Search Courses (Authenticated)'),
    path('/<slug:pk>', views_protected_courses.single_course_view, name='Get single course (Authenticated)'),
]

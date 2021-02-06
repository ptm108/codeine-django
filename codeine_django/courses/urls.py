from django.urls import path

from . import views_course

urlpatterns = [
    path('', views_course.course_view, name='Get all/Search Courses'),
]

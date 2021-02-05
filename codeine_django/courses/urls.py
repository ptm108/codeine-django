from django.urls import path

from . import views_course

urlpatterns = [
    path('', views_course.course_view, name='Get all/Search Courses'),
    path('/<slug:pk>', views_course.single_course_view, name='Get/Update/Delete single course'),
    path('/<slug:pk>/chapters', views_course.course_view, name='Get all/Search Courses'),
    path('/<slug:pk>/sections', views_course.course_view, name='Get all/Search Courses'),
]

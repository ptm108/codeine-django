from django.urls import path

from . import views_course, views_chapters, views_course_materials

urlpatterns = [
    # order views
    path('', views_course.course_view, name='Get all/Search Courses, Create Course'),
    path('/<slug:pk>', views_course.single_course_view, name='Get/Update/Delete single course'),
    path('/<slug:pk>/publish', views_course.publish_course_view, name='Publish a course'),
    path('/<slug:pk>/unpublish', views_course.unpublish_course_view, name='Unpublish a course'),

    # chapter views
    path('/<slug:pk>/chapters', views_chapters.chapter_view, name='Get all/Search Chapters, Create Chapter'),
    path('/<slug:pk>/chapters/<slug:chapter_id>', views_chapters.single_chapter_view, name='Get/Update/Delete single Chapter'),
    path('/<slug:pk>/orderChapters', views_chapters.order_chapter_view, name='Order chapters'),
]

from django.urls import path

from . import views_course, views_chapters, views_course_materials, views_enrollment, views_course_review

urlpatterns = [
    # order views
    path('', views_course.course_view, name='Get all/Search Courses, Create Course'),
    path('/<slug:pk>', views_course.single_course_view, name='Get/Update/Delete single course'),
    path('/<slug:pk>/publish', views_course.publish_course_view, name='Publish a course'),
    path('/<slug:pk>/unpublish', views_course.unpublish_course_view, name='Unpublish a course'),
    path('/<slug:course_id>/activate', views_course.activate_course_view, name='Admin activate a course'),
    path('/<slug:course_id>/deactivate', views_course.deactivate_course_view, name='Admin deactivate a course'),

    # chapter views
    path('/<slug:pk>/chapters', views_chapters.chapter_view, name='Get all/Search Chapters, Create Chapter'),
    path('/<slug:pk>/chapters/<slug:chapter_id>', views_chapters.single_chapter_view, name='Get/Update/Delete single Chapter'),
    path('/<slug:pk>/orderChapters', views_chapters.order_chapter_view, name='Order chapters'),

    # final assessment views
    path('/<slug:course_id>/assessments', views_course.assessment_view, name='Create a course assessment'),
    path('/<slug:course_id>/assessments/<slug:assessment_id>', views_course.single_assessment_view, name='Updates/Deletes a course assessment'),

    # enrollment views
    path('/<slug:course_id>/enrollments', views_enrollment.course_enrollment_views, name='Enroll/Unenroll member'),

    # course review views
    path('/<slug:course_id>/reviews', views_course_review.course_review_views, name='Get all/Search Course Reviews, Create Course Review'),
    path('/<slug:course_id>/reviews/<slug:review_id>', views_course_review.single_course_review_view, name='Get/Update/Delete Course Review'),
]

from django.urls import path

from . import views_course_analytics

urlpatterns = [
    # analytics views
    path('', views_course_analytics.post_log_view, name='Create Event Log'),
    path('/course-conversion-rate', views_course_analytics.course_conversion_rate_view, name='Course conversion metrics'),
    path('/course-material-time', views_course_analytics.course_material_average_time_view, name='Course material time metrics'),
    path('/course-time', views_course_analytics.course_average_time_view, name='Course time metrics'),
    path('/inactive-members', views_course_analytics.inactive_members_view, name='Get inactive members by course'),
    path('/course-members-stats', views_course_analytics.course_member_stats_view, name='Get member stats by course'),
]

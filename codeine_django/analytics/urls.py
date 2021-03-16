from django.urls import path

from . import views_course_analytics, views_earnings, views_search_analytics, views_members_analytics

urlpatterns = [
    # analytics views
    path('', views_course_analytics.post_log_view, name='Create Event Log'),
    path('/course-conversion-rate', views_course_analytics.course_conversion_rate_view, name='Course conversion metrics'),
    path('/course-material-time', views_course_analytics.course_material_average_time_view, name='Course material time metrics'),
    path('/course-time', views_course_analytics.course_average_time_view, name='Course time metrics'),
    path('/inactive-members', views_course_analytics.inactive_members_view, name='Get inactive members by course'),
    path('/course-members-stats', views_course_analytics.course_member_stats_view, name='Get member stats by course'),
    path('/members-demographics', views_course_analytics.member_demographics_view, name='Get member demographics by course/partner'),
    path('/earnings-report', views_earnings.earnings_report_view, name='Get partner\'s earnings report'),
    path('/course-search-ranking', views_search_analytics.course_search_ranking_view, name='Get popular course searches'),
    path('/course-assessment-performance', views_members_analytics.course_assessment_performance_view, name='Get course assessment performance'),

    # EP
    path('/ip-viewer-average-skill', views_members_analytics.viewer_average_skill_view, name='Get average skills of members viewing IP'),
    path('/ip-applicant-average-skill', views_members_analytics.applicant_average_skill_view, name='Get average skills of IP applicants'),
    path('/ip-applicant-demographics', views_members_analytics.applicant_demographics_view, name='Get demographics of IP applicants'),
    path('/ip-search-ranking', views_search_analytics.ip_search_ranking_view, name='Get popular IP searches'),
    path('/ip-application-rate', views_members_analytics.ip_application_rate_view, name='conversion rate for Ip applications'),
]

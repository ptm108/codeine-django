from django.urls import path

from . import views_course_analytics, views_earnings, views_search_analytics, views_members_analytics, views_industry_projects, view_platform_analytics

urlpatterns = [
    # analytics views
    path('', views_course_analytics.post_log_view, name='Create Event Log'),
    path('/course-conversion-rate', views_course_analytics.course_conversion_rate_view, name='Course conversion metrics'),
    path('/course-material-time', views_course_analytics.course_material_average_time_view, name='Course material time metrics'),
    path('/course-time', views_course_analytics.course_average_time_view, name='Course time metrics'),
    path('/inactive-members', views_course_analytics.inactive_members_view, name='Get inactive members by course'),
    path('/course-members-stats', views_course_analytics.course_member_stats_view, name='Get member stats by course'),
    path('/members-demographics', views_course_analytics.member_demographics_view, name='Get member demographics by course/partner'),
    path('/partner-earnings-report', views_earnings.partner_earnings_report_view, name='Get partner\'s earnings report'),
    path('/course-search-ranking', views_search_analytics.course_search_ranking_view, name='Get popular course searches'),
    path('/course-assessment-performance', views_members_analytics.course_assessment_performance_view, name='Get course assessment performance'),

    # EP
    path('/ip-viewer-average-skill', views_industry_projects.viewer_average_skill_view, name='Get average skills of members viewing IP'),
    path('/ip-applicant-average-skill', views_industry_projects.applicant_average_skill_view, name='Get average skills of IP applicants'),
    path('/ip-applicant-demographics', views_industry_projects.applicant_demographics_view, name='Get demographics of IP applicants'),
    path('/ip-search-ranking', views_search_analytics.ip_search_ranking_view, name='Get popular IP searches'),
    path('/ip-application-rate', views_industry_projects.ip_application_rate_view, name='conversion rate for IP applications'),
    path('/ip-popular-skills', views_industry_projects.ip_popular_skills_view, name='popular required skills in IPs'),

    # members
    path('/time-spent-breakdown', views_members_analytics.time_spent_breakdown_view, name='time spent by member on subjects'),

    # admin
    path('/first-enrollment-count', views_course_analytics.course_first_enrollment_count_view, name='get courses with most number of first enrollments'),
    path('/admin-earnings-report', views_earnings.admin_earnings_report_view, name='Admin earnings report'),
    path('/platform-health-check', view_platform_analytics.platform_health_check_view, name='Platform health check'),
]

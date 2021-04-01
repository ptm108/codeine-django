"""codeine_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views_auth import authenticate_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # auth end points
    path('api/token/', authenticate_user, name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # common infra endpoints
    path('auth/', include('common.urls'), name='Common infra end points'),
    path('members/', include('common.urls_member_profile'),
         name='Public member endpoints'),

    # consultation endpoints
    path('consultations', include('consultations.urls_consultations'),
         name='Consultation end points'),
    # path('payments', include('consultations.urls_contribution_payments'), name='Contributions end points'),

    # courses endpoints
    path('courses', include('courses.urls'), name='Courses endpoints'),
    path('chapters', include('courses.urls_chapters'), name='Chapter endpoints'),
    path('materials', include('courses.urls_course_materials'),
         name='Course Materials endpoints'),
    path('private-courses', include('courses.urls_protected_courses'),
         name='Private courses endpoints'),
    path('course-comments', include('courses.urls_course_comments'),
         name='Course Comment endpoints'),

    # quiz endpoints
    path('quiz', include('courses.urls_quiz'),
         name='Quiz and question endpoints'),
    path('quiz-results', include('courses.urls_quiz_results'),
         name='QuizResult endpoints'),
    path('question-banks', include('courses.urls_question_banks'),
         name='Question Bank endpoints'),

    # enrollment endpoints
    path('enrollments', include('courses.urls_enrollments'),
         name='Get/Search Enrollments'),
    path('enrolled-members', include('courses.urls_enrolled_members'),
         name='Get Enrolled Members'),

    # helpdesk endpoints
    path('helpdesk', include('helpdesk.urls'), name='Helpdesk endpoints'),

    # achievements endpoints
    path('achievements', include('achievements.urls'),
         name='Achievements endpoints'),

    # article endpoints
    path('articles', include('community.urls_articles'), name='Article endpoints'),

    # industry projects endpoints
    path('industry-projects', include('industry_projects.urls'),
         name='Industry Projects endpoints'),

    # code review endpoints
    path('code-reviews', include('community.urls_code_reviews'),
         name='Code Review endpoints'),

    # organization end points
    path('events', include('organization.urls_events'), name='Event endpoints'),
    path('contributions', include(
        'organization.urls_contribution_payments'), name='Contribution endpoints'),

    # IDE views
    path('ide', include('common.urls_ide'), name='IDE endpoints'),

    # Analytics views
    path('analytics', include('analytics.urls'), name='Analytics endpoints'),

    # Notifications views
    path('notifications', include('notifications.urls_notifications'),
         name='Notification endpoints'),
    path('notification-objects', include('notifications.urls_notification_objects'),
         name='Notification endpoints'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

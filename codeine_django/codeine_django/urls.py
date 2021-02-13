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

    # content provider endpoints
    path('consultations', include('consultations.urls'), name='Consultation end points'),

    # courses endpoints
    path('courses', include('courses.urls'), name='Courses endpoints'),
    path('chapters', include('courses.urls_chapters'), name='Chapter endpoints'),
    path('materials', include('courses.urls_course_materials'), name='Course Materials endpoints'),

    # tickets endpoints
    path('tickets', include('tickets.urls'), name='Tickets endpoints'),

    # article endpoints
    path('articles', include('community.urls'), name='Article endpoints')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

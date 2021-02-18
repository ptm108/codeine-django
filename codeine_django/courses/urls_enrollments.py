from django.urls import path

from . import views_enrollment

urlpatterns = [
    path('', views_enrollment.enrollment_views, name='Get/Search Enrollments view'),
]

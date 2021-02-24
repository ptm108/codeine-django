from django.urls import path

from . import views_enrollment

urlpatterns = [
    path('', views_enrollment.partner_enrollments_view, name='Get all Enrolled Members'),
]

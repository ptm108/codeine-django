from django.urls import path

from . import views_industry_project, views_application

urlpatterns = [
    # industry projects views
    path('', views_industry_project.industry_project_view, name='Get all/Search/Create Industry Projects'),
    path('/<slug:pk>', views_industry_project.single_industry_project_view, name='Read/Update/Delete/Make Available a Industry Project'),

    # application views
    path('/<slug:pk>/applications', views_application.application_view, name='Get All by Applications by Industry Project/Create Application'),
    path('/applications/member', views_application.member_application_view, name='Get All by Applications by Member'),
    path('/<slug:pk>/applications/<slug:app_id>', views_application.single_application_view, name='Read/Accept Application'),
    path('/<slug:pk>/applications/<slug:app_id>/delete', views_application.delete_application_view, name='Delete Application'),
]

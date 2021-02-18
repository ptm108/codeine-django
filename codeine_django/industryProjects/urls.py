from django.urls import path

from . import views

urlpatterns = [
    # industry projects views
    path('', views.industry_project_view, name='Get all/Search/Create Industry Projects'),
    path('/<slug:pk>', views.single_industry_project_view, name='Read/Update/Delete/Make Available a Industry Project'),
]

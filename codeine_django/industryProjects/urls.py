from django.urls import path

from . import views

urlpatterns = [
    # industry projects views
    path('', views.industry_project_view, name='Get all/Search/Create Industry Projects'),
]

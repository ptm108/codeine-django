from django.urls import path

from . import views

urlpatterns = [
    path('', views.achievement_view, name='Get All/Search/Create Achievement'),
    path('/<slug:pk>', views.single_achievement_view, name='Read/Update/Delete Achievement'),
]
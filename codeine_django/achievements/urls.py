from django.urls import path

from . import views_achievement, views_requirement

urlpatterns = [
    # achivement views
    path('', views_achievement.achievement_view, name='Get All/Search/Create Achievement'),
    path('/<slug:pk>', views_achievement.single_achievement_view, name='Read/Update/Delete Achievement'),

    # achievement requirement views
    path('/<slug:pk>/requirements', views_requirement.achievement_requirement_view, name='Get All by Achievement/Create Achievement Requirement/Delete all Requirement by Achievement'),
    path('/<slug:pk>/requirements/<slug:req_id>', views_requirement.single_achievement_requirement_view, name='Read/Update/Delete Achievement Requirement'),
]
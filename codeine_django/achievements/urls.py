from django.urls import path

from . import views_achievement

urlpatterns = [
    # achivement views
    path('', views_achievement.achievement_view, name='Get All/Search/Create Achievement'),
    path('/<slug:pk>', views_achievement.single_achievement_view, name='Read/Update/Delete Achievement'),

]
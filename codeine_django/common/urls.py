from django.urls import path

from . import views_member

urlpatterns = [
  path('members', views_member.create_member, name='Create/Get all/Search Member'),
  path('members/<slug:pk>', views_member.single_member_view, name='RUD for members'),
]
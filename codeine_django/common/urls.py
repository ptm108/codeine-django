from django.urls import path

from . import views_member

urlpatterns = [
  path('createMember', views_member.create_member, name='Create Member'),
  path('members/<slug:pk>', siews_member.single_member_view, name='RUD for members'),
]
from django.urls import path

from . import views_member

urlpatterns = [
  path('members', views_member.member_view, name='Create/Get all/Search Member'),
  path('members/<slug:pk>', views_member.single_member_view, name='Read/update/delete for members'),
  path('members/<slug:pk>/changePassword', views_member.member_change_password_view, name='Member change password'),
]
from django.urls import path

from . import views_member

urlpatterns = [
    path('members', views_member.member_view, name='Create/Get all/Search Member'),
    path('members/<slug:pk>', views_member.single_member_view, name='Read/update/delete for member'),
    path('members/<slug:pk>/changePassword', views_member.member_change_password_view, name='Member change password'),
    path('members/<slug:pk>/activate', views_member.activate_member_view, name='Activates member'),
    path('members/<slug:pk>/deactivate', views_member.deactivate_member_view, name='Deactivate member'),
]

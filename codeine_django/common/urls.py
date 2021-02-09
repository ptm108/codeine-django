from django.urls import path

from . import views_member, views_partners

urlpatterns = [
    # members views
    path('members', views_member.member_view, name='Create/Get all/Search Member'),
    path('members/<slug:pk>', views_member.single_member_view, name='Read/update/delete for member'),
    path('members/<slug:pk>/changePassword', views_member.member_change_password_view, name='Member change password'),
    path('members/<slug:pk>/activate', views_member.activate_member_view, name='Activates member'),

    # partner views
    path('partners', views_partners.partner_view, name='Create/Get all/Search all active partners'),
    path('partners/<slug:pk>', views_partners.single_partner_view, name='Read/update/delete for partners'),
    path('partners/<slug:pk>/changePassword', views_partners.partner_change_password_view, name='Partner change password'),
    path('partners/<slug:pk>/activate', views_partners.activate_partner_view, name='Activates partner'),
]

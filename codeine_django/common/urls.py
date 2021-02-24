from django.urls import path

from . import views_member, views_partners, views_organization, views_admin

urlpatterns = [
    # members views
    path('members', views_member.member_view, name='Create/Get all/Search Member'),
    path('members/<slug:pk>', views_member.single_member_view, name='Read/update/delete for member'),
    path('members/<slug:pk>/change-password', views_member.member_change_password_view, name='Member change password'),
    path('members/<slug:pk>/activate', views_member.activate_member_view, name='Activates member'),

    # partner views
    path('partners', views_partners.partner_view, name='Create/Get all/Search all active partners'),
    path('partners/<slug:pk>', views_partners.single_partner_view, name='Read/update/delete for partners'),
    path('partners/<slug:pk>/change-password', views_partners.partner_change_password_view, name='Partner change password'),
    path('partners/<slug:pk>/activate', views_partners.activate_partner_view, name='Activates partner'),

    # update organization
    path('organizations/<slug:pk>', views_organization.single_organization_view, name='Update organization detail'),

    # admin user views
    path('admins', views_admin.admin_view, name='Get all/Search Admin Users'),
    path('admins/<slug:pk>', views_admin.single_admin_view, name='Read/Update/Change PW/Delete Admin User'),
]

from django.urls import path

from . import views_member, views_partners, views_organization, views_admin, views_bank_detail
from achievements import views_achievement

urlpatterns = [
    # members views
    path('members', views_member.member_view, name='Create/Get all/Search Member'),
    path('members/<slug:pk>', views_member.single_member_view, name='Read/update/delete for member'),
    path('members/<slug:pk>/change-password', views_member.member_change_password_view, name='Member change password'),
    path('members/<slug:pk>/activate', views_member.activate_member_view, name='Activates member'),
    path('members/<slug:pk>/achievements', views_achievement.get_member_achievements, name='Get member\'s achievements'),

    # partner views
    path('partners', views_partners.partner_view, name='Create/Get all/Search all active partners'),
    path('partners/<slug:pk>', views_partners.single_partner_view, name='Read/update/delete for partners'),
    path('partners/<slug:pk>/change-password', views_partners.partner_change_password_view, name='Partner change password'),
    path('partners/<slug:pk>/activate', views_partners.activate_partner_view, name='Activates partner'),

    # bank detail views
    path('bank-details', views_bank_detail.bank_detail_view, name='Create/Get bank detail by partner'),
    path('bank-details/<slug:pk>', views_bank_detail.single_bank_detail_view, name='Update/Delete bank detail'),

    # update organization
    path('organizations/<slug:pk>', views_organization.single_organization_view, name='Update organization detail'),

    # admin user views
    path('admins', views_admin.admin_view, name='Get all/Search Admin Users'),
    path('admins/<slug:pk>', views_admin.single_admin_view, name='Read/Update/Change PW/Delete Admin User'),
]

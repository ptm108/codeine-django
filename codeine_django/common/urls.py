from django.urls import path

from . import views_member, views_content_provider, views_industry_partner, views_codeine_admin

urlpatterns = [
    # members views
    path('members', views_member.member_view, name='Create/Get all/Search Member'),
    path('members/<slug:pk>', views_member.single_member_view, name='Read/update/delete for member'),
    path('members/<slug:pk>/changePassword', views_member.member_change_password_view, name='Member change password'),
    path('members/<slug:pk>/activate', views_member.activate_member_view, name='Activates member'),

    # content provider views
    path('contentProviders', views_content_provider.content_provider_view, name='Create/Get all/Search content provider'),
    path('contentProviders/<slug:pk>', views_content_provider.single_content_provider_view, name='Read/update/delete for content provider'),
    path('contentProviders/<slug:pk>/changePassword', views_content_provider.content_provider_change_password_view, name='Content provider change password'),
    path('contentProviders/<slug:pk>/activate', views_content_provider.activate_content_provider_view, name='Activates content provider'),

    # Industry partners views
    path('industryPartners', views_industry_partner.industry_partner_view, name='Create/Get all/Search Industry Partners'),
    path('industryPartners/<slug:pk>', views_industry_partner.single_industry_partner_view, name='Read/Update/Delete/Change Password for Industry Partner'),
    path('industryPartners/<slug:pk>/admin', views_industry_partner.industry_partner_admin_view, name='Admin Delete/Activates Industry Member'),

    # Admin views
    path('codeineAdmins', views_codeine_admin.admin_view, name='Create/Get all/Search Admins'),
    path('codeineAdmins/<slug:pk>', views_codeine_admin.single_admin_view, name='Read/update/delete for admin'),
    path('codeineAdmins/<slug:pk>/changePassword', views_codeine_admin.admin_change_password_view, name='Admin change password'),
]

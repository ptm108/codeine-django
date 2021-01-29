from django.urls import path

from . import views_member, views_industry_partner

urlpatterns = [
    # members views
    path('members', views_member.member_view, name='Create/Get all/Search Member'),
    path('members/<slug:pk>', views_member.single_member_view, name='Read/update/delete for member'),
    path('members/<slug:pk>/changePassword', views_member.member_change_password_view, name='Member change password'),
    path('members/<slug:pk>/activate', views_member.activate_member_view, name='Activates member'),

    # Industry partners views
    path('industryPartners', views_industry_partner.industry_partner_view, name='Create/Get all/Search Industry Partners'),
    path('industryPartners/<slug:pk>', views_industry_partner.single_industry_partner_view, name='Read/Delete for Industry Partner'),
    path('industryPartners/<slug:pk>/activate', views_industry_partner.activate_industry_partner_view, name='Activates Industry Partner'),
]

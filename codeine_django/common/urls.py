from django.urls import path

from . import views_member, views_partners, views_organization, views_admin, views_bank_detail, views_membership_subscription
from achievements import views_achievement

urlpatterns = [
    # members views
    path('members', views_member.member_view,
         name='Create/Get all/Search Member'),
    path('members/<slug:pk>', views_member.single_member_view,
         name='Read/update/delete for member'),
    path('members/<slug:pk>/change-password',
         views_member.member_change_password_view, name='Member change password'),
    path('members/<slug:pk>/activate',
         views_member.activate_member_view, name='Activates member'),
    path('members/<slug:pk>/achievements',
         views_achievement.get_member_achievements, name='Get member\'s achievements'),
    path('members/<slug:pk>/suspend', views_member.suspend_user_view,
         name='Suspend/Unsuspend member'),

    # membership-subscriptions views
    path('membership-subscriptions', views_membership_subscription.membership_subscription_view,
         name='Create/Get all/Search Subscription Payments'),
    path('membership-subscriptions/<slug:pk>',
         views_membership_subscription.single_membership_subscription_view, name='Get Subscription Payment'),
    path('membership-subscriptions/<slug:pk>/update',
         views_membership_subscription.update_membership_subscription_view, name='Update Subscription Payment Status'),

    # reset members pw views
    path('reset-password', views_member.reset_member_password_view,
         name='get the refresh token/reset member password'),

    # partner views
    path('partners', views_partners.partner_view,
         name='Create/Get all/Search all active partners'),
    path('partners/<slug:pk>', views_partners.single_partner_view,
         name='Read/update/delete for partners'),
    path('partners/<slug:pk>/change-password',
         views_partners.partner_change_password_view, name='Partner change password'),
    path('partners/<slug:pk>/activate',
         views_partners.activate_partner_view, name='Activates partner'),
    path('partners/<slug:pk>/suspend', views_partners.suspend_user_view,
         name='Suspend/Unsuspend partner'),

    # bank detail views
    path('bank-details', views_bank_detail.bank_detail_view,
         name='Create/Get bank detail by partner'),
    path('bank-details/<slug:pk>', views_bank_detail.single_bank_detail_view,
         name='Update/Delete bank detail'),

    # update organization
    path('organizations/<slug:pk>', views_organization.single_organization_view,
         name='Update organization detail'),

    # admin user views
    path('admins', views_admin.admin_view, name='Get all/Search Admin Users'),
    path('admins/<slug:pk>', views_admin.single_admin_view,
         name='Read/Update/Change PW/Delete Admin User'),
]

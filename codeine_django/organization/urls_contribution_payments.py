from django.urls import path

from . import views_contribution_payment

urlpatterns = [
    # contribution payment views
    path('', views_contribution_payment.contribution_payment_view, name='Create/Get all/Search Contribution Payments'),
    path('/<slug:pk>', views_contribution_payment.single_contribution_payment_view, name='Get Contribution Payment'),
    path('/<slug:pk>/update', views_contribution_payment.update_contribution_payment_view, name='Update Contribution Payment Status'),
]

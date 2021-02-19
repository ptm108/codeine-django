from django.urls import path

from . import views_contribution_payment

urlpatterns = [
    # payment transaction views
    # path('', views_contribution_payment.payment_transaction_view, name='Create/Get all/Search payment transaction'),
    # path('/<slug:pk>', views_contribution_payment.single_payment_transaction_view, name='Read/update/delete for payment transaction')
]

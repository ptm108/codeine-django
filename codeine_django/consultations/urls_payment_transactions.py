from django.urls import path

from . import views_payment_transaction

urlpatterns = [
    # payment transaction views
    path('/<slug:consultation_slot_id>', views_payment_transaction.payment_transaction_view, name='Create/Get all/Search payment transaction'),
    path('/<slug:pk>', views_payment_transaction.single_payment_transaction_view, name='Read/update/delete for payment transaction')
]

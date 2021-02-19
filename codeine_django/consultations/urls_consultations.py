from django.urls import path

from . import views_consultation, views_consultation_payment

urlpatterns = [
    # consultation views
    path('', views_consultation.consultation_slot_view, name='Create/Get all/Search Consultation'),
    path('/<slug:pk>', views_consultation.single_consultation_slot_view, name='Read/update/delete for consultation'),
    path('/<slug:pk>/confirm', views_consultation.confirm_consultation_slot, name='Confirm a slot for consultation'),
    path('/<slug:pk>/reject', views_consultation.reject_consultation_slot, name='Partner rejects slot for consultation'),
    path('/<slug:pk>/apply', views_consultation.apply_consultation_slot, name='Member cancels slot for consultation'),
    path('/<slug:pk>/cancel', views_consultation.cancel_consultation_slot, name='Member cancels slot for consultation'),

    # consultation payment transaction views
    path('/<slug:pk>/payment', views_consultation_payment.consultation_payment_view, name='Create/Get all/Search Payment Transaction for Consultations'),
]

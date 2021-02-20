from django.urls import path

from . import views_consultation, views_consultation_application, views_consultation_payment

urlpatterns = [
    # consultation slot views
    path('', views_consultation.consultation_slot_view, name='Create/Get all/Search Consultation'),
    path('/<slug:pk>', views_consultation.single_consultation_slot_view, name='Read/update/delete for consultation'),
    path('/<slug:pk>/cancel', views_consultation.cancel_consultation_slot, name='Partner cancels slot for consultation'),
    # path('/<slug:pk>/confirm', views_consultation.confirm_consultation_slot, name='Confirm a slot for consultation'),

    # consultation application views
    path('/<slug:consultation_slot_id>/apply', views_consultation_application.consultation_application_view, name='Member Create/ Get/ Search Consultation Applications for a single consultation slot'),
    path('/application/<slug:pk>', views_consultation_application.single_consultation_application_view, name='Get consultation applicatio by id'),
    path('/application/<slug:pk>/cancel', views_consultation_application.cancel_consultation_application, name='Member cancels consultation application'),

    # consultation payment transaction views
    path('/application/<slug:consultation_application_id>/payment', views_consultation_payment.consultation_payment_view, name='Create/Get all/Search Payment Transaction for a Consultation Application'),
]

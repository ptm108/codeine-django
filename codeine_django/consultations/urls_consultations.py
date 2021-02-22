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
    path('/application/<slug:pk>', views_consultation_application.single_consultation_application_view, name='Get consultation application by id'),
    path('/application/<slug:pk>/cancel', views_consultation_application.cancel_consultation_application, name='Member cancels consultation application'),
    path('/partner/applications', views_consultation_application.partner_consultation_application_view, name='Partner Get/ Search consultation applications'),

    # consultation payment transaction views
    path('/application/<slug:consultation_application_id>/payment', views_consultation_payment.consultation_payment_view, name='Create/Get all/Search Consultation Payment Transaction for a Consultation Application'),
    path('/payment/<slug:pk>', views_consultation_payment.single_consultation_payment_view, name='Get Consultation Payment Transaction by ID'),
    path('/payment/<slug:pk>/update', views_consultation_payment.update_consultation_payment_status, name='Update Consultation Payment Transaction Status'),
]

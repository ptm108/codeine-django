from django.urls import path

from . import views_consultation

urlpatterns = [
    # consultation views
    path('consultations', views_consultation.consultation_slot_view, name='Create/Get all/Search Consultation'),
    path('consultations/<slug:pk>', views_consultation.single_consultation_slot_view, name='Read/update/delete for consultation'),
    path('consultations/<slug:pk>/confirm', views_consultation.confirm_consultation_slot, name='Confirm a slot for consultation and enter meeting link'),
]

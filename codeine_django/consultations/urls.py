from django.urls import path

from . import views_consultation

urlpatterns = [
    # consultation views
    path('', views_consultation.consultation_slot_view, name='Create/Get all/Search Consultation'),
    path('/<slug:pk>', views_consultation.single_consultation_slot_view, name='Read/update/delete for consultation'),
    path('/<slug:pk>/confirm', views_consultation.confirm_consultation_slot, name='Confirm a slot for consultation'),
    path('/<slug:pk>/reject', views_consultation.reject_consultation_slot, name='Reject slot for consultation')
]

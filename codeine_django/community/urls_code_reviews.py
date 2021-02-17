from django.urls import path

from . import views_code_review

urlpatterns = [
    # code review views
    path('', views_code_review.code_review_view, name='Create/Get all/Search Code Reviews'),
    path('/<slug:pk>', views_code_review.single_code_review_view, name='Read/update/delete for Code Review')
]

from django.urls import path

from . import views_quiz_result

urlpatterns = [
    # Quiz views
    path('/<slug:quiz_result_id>', views_quiz_result.update_quiz_result_view, name='Update quiz response'),
    path('/<slug:quiz_result_id>/submit', views_quiz_result.sumbit_quiz_result_view, name='Submit quiz'),
]

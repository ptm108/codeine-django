from django.urls import path

from . import views_quiz, views_quiz_result

urlpatterns = [
    # Quiz views
    path('/<slug:qb_id>/questions', views_quiz.add_question_view, name='Add question'),
    path('/<slug:qb_id>/questions/<slug:question_id>', views_quiz.single_question_view, name='Add question'),
    path('/<slug:qb_id>/order-questions', views_quiz.order_question_view, name='set order of questions'),
]

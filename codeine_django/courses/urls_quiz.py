from django.urls import path

from . import views_quiz

urlpatterns = [
    # course material views
    path('/<slug:quiz_id>', views_quiz.quiz_view, name='Get quiz by id'),
    path('/<slug:quiz_id>/questions', views_quiz.add_question_view, name='Add question'),
    path('/<slug:quiz_id>/questions/<slug:question_id>', views_quiz.single_question_view, name='Add question'),
    path('/<slug:quiz_id>/orderQuestions', views_quiz.order_question_view, name='set order of questions'),
]

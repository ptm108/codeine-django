from django.urls import path

from . import views_quiz, views_quiz_result

urlpatterns = [
    # Quiz views
    path('', views_quiz.all_quiz_view, name='Get all quizzes'),
    path('/<slug:quiz_id>', views_quiz.quiz_view, name='Get quiz by id'),
    # path('/<slug:quiz_id>/question-groups', views_quiz.add_question_view, name='Add questions'),
    # path('/<slug:quiz_id>/questions/<slug:question_id>', views_quiz.single_question_view, name='Add question'),
    # path('/<slug:quiz_id>/order-questions', views_quiz.order_question_view, name='set order of questions'),

    # quiz result views
    path('/<slug:quiz_id>/results', views_quiz_result.quiz_result_views, name='Create/Submit quiz result'),

    # question group view
    path('/<slug:quiz_id>/question-groups', views_quiz.delete_question_group_view, name='Delete question group'),
]

from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Sum, Avg, Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)

from datetime import timedelta

from .models import EventLog
from common.permissions import IsPartnerOrAdminOnly
from common.models import Partner, Member, BaseUser
from courses.models import QuizResult, Course, CourseMaterial
from utils.member_utils import get_average_skill_set
from industry_projects.models import IndustryProject, IndustryProjectApplication


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def course_assessment_performance_view(request):
    '''
    Gets the assessment performance of enrolled members
    by partner or overall
    '''
    if request.method == 'GET':
        user = request.user

        try:
            days = int(request.query_params.get('days', 120))
            now = timezone.now()
            quiz_results = QuizResult.objects.filter(date_created__date__gte=now - timedelta(days=days))
            courses = Course.objects

            partner = Partner.objects.filter(user=user).first()
            if partner is not None:
                courses = courses.filter(partner=partner)
            # end if

            res = {
                'overall_average_score': 0,
                'overall_passing_rate': 0,
                'breakdown_by_course': []
            }
            active_courses = 0

            courses = courses.all()
            for course in courses:
                tmp_course = {
                    'course_id': course.id,
                    'course_title': course.title,
                    'average_score': None,
                    'passing_rate': None,
                    'course_material_quiz': []
                }
                course_quiz_results = quiz_results.filter(quiz__course=course).filter(submitted=True)

                if len(course_quiz_results) <= 0:
                    res['breakdown_by_course'].append(tmp_course)
                    continue
                # end if

                active_courses += 1

                average_score = course_quiz_results.aggregate(Avg('score'))
                total_score = course_quiz_results.annotate(total_score=Sum('quiz__question_groups__question_bank__questions__shortanswer__marks') + Sum('quiz__question_groups__question_bank__questions__mcq__marks') + Sum('quiz__question_groups__question_bank__questions__mrq__marks'))[0].total_score
                # print(average_score['score__avg']/total_score)
                tmp_course['average_score'] = average_score['score__avg'] / total_score if total_score > 0 else 0

                passing_rate = len(course_quiz_results.filter(passed=True).all()) / len(course_quiz_results.all()) if len(course_quiz_results.all()) > 0 else 0
                # print(passing_rate)
                tmp_course['passing_rate'] = passing_rate
                res['breakdown_by_course'].append(tmp_course)

                res['overall_average_score'] += average_score['score__avg'] / total_score
                res['overall_passing_rate'] += passing_rate

                course_material_quiz_results = quiz_results.filter(quiz__course_material__chapter__course=course).values('quiz').order_by()
                average_score = course_material_quiz_results.annotate(Avg('score'))
                total_score = course_material_quiz_results.annotate(total_score=Sum('quiz__question_groups__question_bank__questions__shortanswer__marks') + Sum('quiz__question_groups__question_bank__questions__mcq__marks') + Sum('quiz__question_groups__question_bank__questions__mrq__marks'))

                for i in range(len(average_score.all())):
                    cm = CourseMaterial.objects.get(quiz__pk=average_score[i]['quiz'])
                    tmp_cm = {
                        'course_material_id': cm.id,
                        'course_material_title': cm.title,
                        'quiz_id': cm.quiz.id,
                        'average_score': average_score[i]['score__avg'] / total_score[i]['total_score'] if total_score[i]['total_score'] > 0 else 0,
                        'passing_rate': len(course_material_quiz_results.filter(passed=True).all()) / len(course_material_quiz_results.all()) if len(course_material_quiz_results.all()) > 0 else 0
                    }
                    tmp_course['course_material_quiz'].append(tmp_cm)
                # end for

            # quiz_results_total = quiz_results.annotate(total_score=Sum('quiz__questions__shortanswer__marks') + Sum('quiz__questions__mcq__marks') + Sum('quiz__questions__mrq__marks'))
            # quiz_results = quiz_results.values('quiz__course').order_by().annotate(average_score=Avg('score'))
            res['overall_average_score'] = res['overall_average_score'] / active_courses if active_courses > 0 else 0
            res['overall_passing_rate'] = res['overall_passing_rate'] / active_courses if active_courses > 0 else 0

            return Response(res)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ZeroDivisionError as e:
            print(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def time_spent_breakdown_view(request):
    '''
    Get the time member has spent on various subjects
    '''
    if request.method == 'GET':
        user = request.user
        member = Member.objects.filter(user=user).first()

        try:
            if member is None:
                user_id = request.query_params.get('user_id', None)
                user = BaseUser.objects.get(pk=user_id)
            # end if

            days = int(request.query_params.get('days', 9999))
            now = timezone.now()

            stats = {
                'PY': 0,
                'JAVA': 0,
                'JS': 0,
                'CPP': 0,
                'CS': 0,
                'HTML': 0,
                'CSS': 0,
                'RUBY': 0,
                'SEC': 0,
                'DB': 0,
                'FE': 0,
                'BE': 0,
                'UI': 0,
                'ML': 0,
            }

            event_logs = EventLog.objects.filter(timestamp__date__gte=now - timedelta(days=days)).filter(user=member.user)
            event_logs = event_logs.filter(payload='stop course material').exclude(duration=None)

            total_time = 0
            for ev in event_logs:
                duration = ev.duration
                total_time += duration

                course = ev.course_material.chapter.course
                coding_languages = list(course.coding_languages)
                categories = list(course.categories)

                for cl in coding_languages:
                    stats[cl] += duration
                # end for

                for c in categories:
                    stats[c] += duration
                # end for
            # end for
            # print(len(event_logs))

            return Response({
                'total_time_spent': total_time,
                'breakdown_by_categories': stats
            }, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, ValueError, KeyError, ZeroDivisionError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

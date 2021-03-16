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

from common.permissions import IsPartnerOrAdminOnly
from common.models import Partner
from courses.models import QuizResult, Course


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def course_assessment_performance_view(request):
    '''
    Gets the assessment performance of enrolled members
    by partner or by course
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
                }
                course_quiz_results = quiz_results.filter(quiz__course=course).filter(submitted=True)

                if len(course_quiz_results) <= 0:
                    res['breakdown_by_course'].append(tmp_course)
                    continue
                # end if

                active_courses += 1

                average_score = course_quiz_results.aggregate(Avg('score'))
                total_score = course_quiz_results.annotate(total_score=Sum('quiz__questions__shortanswer__marks') + Sum('quiz__questions__mcq__marks') + Sum('quiz__questions__mrq__marks'))[0].total_score
                # print(average_score['score__avg']/total_score)
                tmp_course['average_score'] = average_score['score__avg'] / total_score

                passing_rate = len(course_quiz_results.filter(passed=True).all()) / len(course_quiz_results.all())
                # print(passing_rate)
                tmp_course['passing_rate'] = passing_rate
                res['breakdown_by_course'].append(tmp_course)

                res['overall_average_score'] += average_score['score__avg'] / total_score
                res['overall_passing_rate'] += passing_rate
            # end for

            # quiz_results_total = quiz_results.annotate(total_score=Sum('quiz__questions__shortanswer__marks') + Sum('quiz__questions__mcq__marks') + Sum('quiz__questions__mrq__marks'))
            # quiz_results = quiz_results.values('quiz__course').order_by().annotate(average_score=Avg('score'))
            res['overall_average_score'] /= active_courses
            res['overall_passing_rate'] /= active_courses

            return Response(res)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

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
from industry_projects.models import IndustryProject


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
                total_score = course_quiz_results.annotate(total_score=Sum('quiz__questions__shortanswer__marks') + Sum('quiz__questions__mcq__marks') + Sum('quiz__questions__mrq__marks'))[0].total_score
                # print(average_score['score__avg']/total_score)
                tmp_course['average_score'] = average_score['score__avg'] / total_score

                passing_rate = len(course_quiz_results.filter(passed=True).all()) / len(course_quiz_results.all())
                # print(passing_rate)
                tmp_course['passing_rate'] = passing_rate
                res['breakdown_by_course'].append(tmp_course)

                res['overall_average_score'] += average_score['score__avg'] / total_score
                res['overall_passing_rate'] += passing_rate

                course_material_quiz_results = quiz_results.filter(quiz__course_material__chapter__course=course).values('quiz').order_by()
                average_score = course_material_quiz_results.annotate(Avg('score'))
                total_score = course_material_quiz_results.annotate(total_score=Sum('quiz__questions__shortanswer__marks') + Sum('quiz__questions__mcq__marks') + Sum('quiz__questions__mrq__marks'))

                for i in range(len(average_score.all())):
                    cm = CourseMaterial.objects.get(quiz__pk=average_score[i]['quiz'])
                    tmp_cm = {
                        'course_material_id': cm.id,
                        'course_material_title': cm.title,
                        'quiz_id': cm.quiz.id,
                        'average_score': average_score[i]['score__avg'] / total_score[i]['total_score'],
                        'passing_rate': len(course_material_quiz_results.filter(passed=True).all()) / len(course_material_quiz_results.all())
                    }
                    tmp_course['course_material_quiz'].append(tmp_cm)
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


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def viewer_average_skill_view(request):
    '''
    Get the average skillset of viewers of industry projects
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()
        try:
            industry_project_id = request.query_params.get('industry_project_id', None)

            industry_projects = IndustryProject.objects
            if partner is not None:
                industry_projects = industry_projects.filter(partner=partner)
            # end if
            if industry_project_id is not None:
                industry_projects = industry_projects.filter(pk=industry_project_id)
            # end if

            event_logs = EventLog.objects.filter(
                Q(payload='view industry project') &
                Q(industry_project__in=industry_projects.all())
            ).exclude(
                Q(user__member=None) &
                Q(user=None)
            )

            members = Member.objects.filter(user__event_logs__in=event_logs)
            average_skill_set = get_average_skill_set(members.all())

            res = {
                'unique_member_views': len(members.all()),
                'average_skill_set': average_skill_set,
                'breakdown_by_industry_project': []
            }

            for industry_project in industry_projects:
                tmp_event_logs = event_logs.filter(industry_project=industry_project)
                tmp_members = members.filter(user__event_logs__in=tmp_event_logs)

                tmp_ip = {
                    'ip_id': industry_project.id,
                    'ip_title': industry_project.title,
                    'unique_member_views': len(tmp_members.all()),
                    'average_skill_set': get_average_skill_set(tmp_members),
                }
                res['breakdown_by_industry_project'].append(tmp_ip)
            # end for

            return Response(res, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def applicant_average_skill_view(request):
    '''
    Get the average skillset of applicants of industry projects
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()
        try:
            industry_project_id = request.query_params.get('industry_project_id', None)

            industry_projects = IndustryProject.objects
            if partner is not None:
                industry_projects = industry_projects.filter(partner=partner)
            # end if
            if industry_project_id is not None:
                industry_projects = industry_projects.filter(pk=industry_project_id)
            # end if

            members = Member.objects.filter(industry_project_applications__industry_project__in=industry_projects.all())
            res = {
                'unique_applicants': len(members.all()),
                'average_skill_set': get_average_skill_set(members.all()),
                'breakdown_by_industry_project': []
            }

            for ip in industry_projects:
                tmp_members = members.filter(industry_project_applications__industry_project=ip)
                tmp_ip = {
                    'ip_id': ip.id,
                    'ip_title': ip.title,
                    'unique_member_views': len(tmp_members.all()),
                    'average_skill_set': get_average_skill_set(tmp_members),
                }
                res['breakdown_by_industry_project'].append(tmp_ip)
            # end for

            return Response(res, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def applicant_demographics_view(request):
    '''
    Get the demographics of industry projects applicants
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()
        try:
            industry_project_id = request.query_params.get('industry_project_id', None)

            industry_projects = IndustryProject.objects
            if partner is not None:
                industry_projects = industry_projects.filter(partner=partner)
            # end if
            if industry_project_id is not None:
                industry_projects = industry_projects.filter(pk=industry_project_id)
            # end if

            members = BaseUser.objects.filter(member__industry_project_applications__industry_project__in=industry_projects.all())
            gender = members.values('gender').order_by().annotate(Count('id'))
            location = members.values('location').order_by().annotate(Count('id'))
            age = members.aggregate(Avg('age'))

            res = {
                'genders': gender,
                'locations': location,
                'average_age': age['age__avg'],
                'breakdown_by_industry_project': []
            }

            for ip in industry_projects:
                tmp_members = members.filter(industry_project_applications__industry_project=ip)
                gender = members.values('gender').order_by().annotate(Count('id'))
                location = members.values('location').order_by().annotate(Count('id'))
                age = members.aggregate(Avg('age'))
                tmp_ip = {
                    'ip_id': ip.id,
                    'ip_title': ip.title,
                    'genders': gender,
                    'locations': location,
                    'average_age': age['age__avg'],
                }
                res['breakdown_by_industry_project'].append(tmp_ip)
            # end for

            return Response(res, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

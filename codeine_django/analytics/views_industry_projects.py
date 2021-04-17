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
                tmp_members = members.filter(member__industry_project_applications__industry_project=ip)
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


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def ip_application_rate_view(request):
    '''
    Get conversion rate of ip page views --> applications
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()

        try:
            days = int(request.query_params.get('days', 120))
            now = timezone.now()

            overall_views = EventLog.objects.filter(timestamp__date__gte=now - timedelta(days=days))
            applications = IndustryProjectApplication.objects.filter(date_created__date__gte=now - timedelta(days=days))
            industry_projects = IndustryProject.objects

            if partner is not None:
                industry_projects = industry_projects.filter(partner=partner)
                overall_views = overall_views.filter(industry_project__in=industry_projects.all())
                applications = applications.filter(industry_project__in=industry_projects.all())
            # end if

            view_count = overall_views.count()
            application_count = applications.count()

            res = {}
            res['overall_conversion_rate'] = application_count / view_count if view_count > 0 else 0
            res['overall_views'] = view_count
            res['applications'] = application_count

            breakdown = []
            for ip in industry_projects.all():
                tmp = {}
                tmp['ip_id'] = ip.id
                tmp['ip_title'] = ip.title

                view_count = overall_views.filter(industry_project=ip).count()
                application_count = applications.filter(industry_project=ip).count()
                tmp['conversion_rate'] = application_count / view_count if view_count > 0 else 0
                tmp['view_count'] = view_count
                tmp['application_count'] = application_count

                breakdown.append(tmp)
            # end for
            res['breakdown_by_industry_project'] = breakdown

            return Response(res, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, ValueError, KeyError, ZeroDivisionError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((AllowAny,))
def ip_popular_skills_view(request):
    '''
    Get the most popular skills required in industry projects
    '''
    if request.method == 'GET':
        industry_project_ranking = IndustryProject.objects.values('categories').order_by().annotate(count=Count('id'))
        return Response(industry_project_ranking, status=status.HTTP_200_OK)
    # end if
# end def

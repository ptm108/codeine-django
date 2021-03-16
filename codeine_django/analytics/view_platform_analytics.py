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

from common.models import Member, MembershipSubscription, BaseUser
from courses.models import Course, Enrollment
from consultations.models import ConsultationSlot
from industry_projects.models import IndustryProject


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def platform_health_check_view(request):
    '''
    Hours of content created,
    number of consultation slots opened, 
    projects listed,
    conversion of free to pro tier
    '''
    if request.method == 'GET':
        try:
            days = int(request.query_params.get('days', 30))
            _date = timezone.now() - timedelta(days=days)

            hours_of_content = Course.objects.filter(published_date__date__gte=_date).count()
            new_consultation_slots = ConsultationSlot.objects.filter(start_time__date__gte=_date).count()
            new_industry_projects = IndustryProject.objects.filter(date_listed__date__gte=_date).count()
            new_pro_members = MembershipSubscription.objects.values('member').filter(payment_transaction__timestamp__date__gte=_date).order_by().annotate(Count('id')).filter(id__count=1).count()

            return Response({
                'hours_of_content': hours_of_content,
                'new_consultation_slots': new_consultation_slots,
                'new_industry_projects': new_industry_projects,
                'new_pro_members': new_pro_members,
            }, status=status.HTTP_200_OK)
        except (ValidationError, KeyError, ValueError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def course_enrollment_count_view(request):
    '''
    number of enrollments by course
    '''
    if request.method == 'GET':
        try:
            days = int(request.query_params.get('days', 30))
            partner_id = request.query_params.get('partner_user_id', None)
            _date = timezone.now() - timedelta(days=days)
            partner = BaseUser.objects.filter(pk=partner_id).first()

            enrollments = Enrollment.objects
            if partner is not None:
                enrollments = enrollments.filter(course__partner=partner.partner)
            # end if

            enrollments = enrollments.values('course').order_by().annotate(Count('id')).order_by('-id__count')
            res = []
            for enrollment in enrollments.all():
                course = Course.objects.get(pk=str(enrollment['course']))
                tmp = {
                    'course_id': course.id,
                    'course_title': course.title,
                    'enrollment_count': enrollment['id__count']
                }
                res.append(tmp)
            # end for

            return Response(res, status=status.HTTP_200_OK)
        except (ValidationError, KeyError, ValueError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

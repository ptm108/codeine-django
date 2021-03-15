from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Sum, Avg
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)

from .models import EventLog
from common.permissions import IsPartnerOrAdminOnly
from common.models import Partner
from courses.models import Course, CourseMaterial, Quiz, Enrollment
from industry_projects.models import IndustryProject


@api_view(['POST'])
@permission_classes((AllowAny,))
def post_log_view(request):
    user = request.user
    '''
    Creates a new log
    '''
    if request.method == 'POST':
        data = request.data

        course = Course.objects.get(pk=data['course']) if 'course' in data else None
        course_material = CourseMaterial.objects.get(pk=data['course_material']) if 'course_material' in data else None
        quiz = Quiz.objects.get(data['quiz']) if 'quiz' in data else None
        industry_project = IndustryProject.objects.get(data['industry_project']) if 'industry_project' in data else None

        try:
            with transaction.atomic():
                event_log = EventLog(
                    payload=data['payload'],
                    user=user if user.is_authenticated else None,
                    course=course,
                    course_material=course_material,
                    quiz=quiz,
                    industry_project=industry_project,
                )

                # duration logging for course material
                if data['payload'] == 'stop course material':
                    stop_event = EventLog.objects.filter(
                        Q(payload='stop course material') &
                        Q(course_material=course_material) &
                        Q(user=request.user)
                    ).first()
                    continue_event = EventLog.objects.filter(
                        Q(payload='continue course material') &
                        Q(course_material=course_material) &
                        Q(user=request.user)
                    )

                    if stop_event is not None:
                        continue_event = continue_event.filter(timestamp__gte=stop_event.timestamp).filter(course_material=course_material).last()
                    else:
                        continue_event = continue_event.first()
                    # end if-else

                    if continue_event is not None:
                        event_log.duration = timezone.now().timestamp() - continue_event.timestamp.timestamp()
                    # end if
                # end if

                # duration logging for course
                if data['payload'] == 'stop course':
                    stop_event = EventLog.objects.filter(
                        Q(payload='stop course') &
                        Q(course_material=course_material) &
                        Q(user=request.user)
                    ).first()
                    continue_event = EventLog.objects.filter(
                        Q(payload='continue course') &
                        Q(course_material=course_material) &
                        Q(user=request.user)
                    )

                    if stop_event is not None:
                        continue_event = continue_event.filter(timestamp__gte=stop_event.timestamp).filter(course_material=course_material).last()
                    else:
                        continue_event = continue_event.first()
                    # end if-else

                    if continue_event is not None:
                        event_log.duration = timezone.now().timestamp() - continue_event.timestamp.timestamp()
                    # end if
                # end if

                # duration logging for assessments
                if data['payload'] == 'stop assessment':
                    stop_event = EventLog.objects.filter(
                        Q(payload='stop assessment') &
                        Q(course_material=course_material) &
                        Q(user=request.user)
                    ).first()
                    continue_event = EventLog.objects.filter(
                        Q(payload='continue assessment') &
                        Q(course_material=course_material) &
                        Q(user=request.user)
                    )

                    if stop_event is not None:
                        continue_event = continue_event.filter(timestamp__gte=stop_event.timestamp).filter(course_material=course_material).last()
                    else:
                        continue_event = continue_event.first()
                    # end if-else

                    if continue_event is not None:
                        event_log.duration = timezone.now().timestamp() - continue_event.timestamp.timestamp()
                    # end if
                # end if

                event_log.save()
            # end with
            return Response(status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError, ValidationError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@ api_view(['GET'])
@ permission_classes((IsPartnerOrAdminOnly,))
def course_conversion_rate_view(request):
    '''
    Get conversion rate of course page views --> enrollments
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()

        try:
            overall_view = EventLog.objects
            enrollments = Enrollment.objects

            period = request.query_params.get('period', None)
            now = timezone.now()

            if period == 'day':
                overall_view = overall_view.filter(timestamp__date=now)
                enrollments = enrollments.filter(date_created__date=now)
            elif period == 'week':
                week = now.isocalendar()[1]
                overall_view = overall_view.filter(timestamp__week=week)
                enrollments = enrollments.filter(date_created__week=week)
            elif period == 'month':
                overall_view = overall_view.filter(timestamp__month=now.month)
                enrollments = enrollments.filter(date_created__month=now.month)
            elif period == 'year':
                overall_view = overall_view.filter(timestamp__year=now.year)
                enrollments = enrollments.filter(date_created__year=now.year)
            # end if-else

            if not user.is_admin and partner is not None:
                overall_view = overall_view.filter(course__partner=partner)
                enrollments = enrollments.filter(course__partner=partner)
            # end if

            view_count = overall_view.count()
            enrollment_count = enrollments.count()

            res = {}
            res['overall_conversion_rate'] = enrollment_count / view_count if view_count > 0 else 0
            res['overall_view'] = view_count
            res['enrollments'] = enrollment_count

            breakdown = []
            for course in partner.courses.all():
                tmp = {}
                tmp['course_id'] = course.id
                tmp['title'] = course.title
                view_count = overall_view.filter(course=course).count()
                enrollment_count = enrollments.filter(course=course).count()
                tmp['conversion_rate'] = enrollment_count / view_count if view_count > 0 else 0
                tmp['view_count'] = view_count
                tmp['enrollment_count'] = enrollment_count

                breakdown.append(tmp)
            # end for
            res['breakdown'] = breakdown

            return Response(res, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, ValueError, KeyError, ZeroDivisionError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@ api_view(['GET'])
@ permission_classes((IsPartnerOrAdminOnly,))
def course_material_average_time_view(request):
    '''
    Calculates average time spent on course material in a course
    '''
    if request.method == 'GET':
        try:
            course_id = request.query_params.get('course_id', None)
            course = Course.objects.get(pk=course_id)

            res = {
                'course_id': course.id,
                'course_title': course.title,
                'course_image': request.build_absolute_uri(course.thumbnail.url),
                'chapters': []
            }
            total_time = 0
            for chapter in course.chapters.all():
                tmp_chap = {
                    'chapter_id': chapter.id,
                    'chapter_title': chapter.title,
                    'course_materials': []
                }

                for cm in chapter.course_materials.all():
                    tmp_cm = {
                        'course_material_id': cm.id,
                        'course_material_title': cm.title,
                        'material_type': cm.material_type
                    }
                    average_time = EventLog.objects.filter(Q(course_material=cm) & Q(payload='stop course material')).exclude(duration=None).values('user').annotate(total_time=Sum('duration')).order_by().aggregate(Avg('total_time'))
                    # print(average_time)
                    tmp_cm['average_time_taken'] = average_time['total_time__avg']

                    tmp_chap['course_materials'].append(tmp_cm)
                # end for

                res['chapters'].append(tmp_chap)
            # end for

            return Response(res, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, KeyError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Sum, Avg, Count, F
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
from .serializers import EventLogSerializer
from common.permissions import IsPartnerOrAdminOnly
from common.models import Partner, Member, BaseUser
from common.serializers import NestedBaseUserSerializer
from courses.models import Course, CourseMaterial, Quiz, Enrollment
from courses.serializers import CourseSerializer
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
        query_params = request.query_params

        course = Course.objects.filter(pk=query_params.get('course_id', None)).first()
        course_material = CourseMaterial.objects.filter(pk=query_params.get('course_material_id', None)).first()
        quiz = Quiz.objects.filter(pk=query_params.get('quiz_id', None)).first()
        industry_project = IndustryProject.objects.filter(pk=query_params.get('industry_project_id', None)).first()
        search_string = query_params.get('search_string', None)

        try:
            with transaction.atomic():
                event_log = EventLog(
                    payload=data['payload'],
                    user=user if user.is_authenticated else None,
                    course=course,
                    course_material=course_material,
                    quiz=quiz,
                    industry_project=industry_project,
                    search_string=search_string
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


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
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

            days = int(request.query_params.get('days', 120))
            now = timezone.now()

            overall_view = overall_view.filter(timestamp__date__gte=now - timedelta(days=days))
            enrollments = enrollments.filter(date_created__date__gte=now - timedelta(days=days))
            total_enrollments = Enrollment.objects

            if partner is not None:
                overall_view = overall_view.filter(course__partner=partner)
                enrollments = enrollments.filter(course__partner=partner)
                total_enrollments = total_enrollments.filter(course__partner=partner)
            # end if

            view_count = overall_view.count()
            enrollment_count = enrollments.count()

            res = {}
            res['overall_conversion_rate'] = enrollment_count / view_count if view_count > 0 else 0
            res['overall_view'] = view_count
            res['enrollments'] = enrollment_count
            res['total_enrollments'] = total_enrollments.count()

            breakdown = []
            courses = partner.courses.all() if partner is not None else Course.objects.all()
            for course in courses:
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


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def course_material_average_time_view(request):
    '''
    Calculates average time spent on course material in a course
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()

        try:
            course_id = request.query_params.get('course_id', None)

            courses = Course.objects.filter(partner=partner) if partner is not None else Course.objects
            course = courses.get(pk=course_id)

            res = {
                'course_id': course.id,
                'course_title': course.title,
                'course_image': request.build_absolute_uri(course.thumbnail.url),
                'chapters': []
            }

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
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def course_average_time_view(request):
    '''
    Calculates average time spent on a course
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()

        try:
            course_id = request.query_params.get('course_id', None)

            courses = Course.objects.filter(partner=partner) if partner is not None else Course.objects
            course = courses.get(pk=course_id)

            event_logs = EventLog.objects.filter(
                Q(course=course) &
                Q(payload='stop course')
            ).exclude(duration=None)

            average_time = event_logs.values('user').annotate(total_time=Sum('duration')).order_by().aggregate(Avg('total_time'))

            return Response({'course_id': course.id, 'course_title': course.title, 'description': course.description, 'average_time_taken': average_time['total_time__avg']}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError, ValidationError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def inactive_members_view(request):
    '''
    Gets a list of inactive members in a course
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()

        try:
            course_id = request.query_params.get('course_id', None)
            days = int(request.query_params.get('days', 7))

            courses = Course.objects.filter(partner=partner) if partner is not None else Course.objects
            course = courses.get(pk=course_id)

            inactive_members = []
            today = timezone.now() - timedelta(days=days)

            for enrollment in course.enrollments.all():
                event_logs = EventLog.objects.filter(user=enrollment.member.user).filter(
                    Q(course=course) |
                    Q(course_material__chapter__course=course)
                )
                event_log = event_logs.filter(timestamp__gte=today).first()

                if event_log is not None:
                    continue
                # end if

                event_log = EventLog.objects.filter(user=enrollment.member.user).first()
                user_data = NestedBaseUserSerializer(enrollment.member.user, context={"request": request}).data
                inactive_members.append({**user_data, 'last_active': event_log.timestamp})
            # end for

            return Response(inactive_members, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def course_member_stats_view(request):
    '''
    Get percentage of false starters and active members in course
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()

        try:
            course_id = request.query_params.get('course_id', None)
            days = int(request.query_params.get('days', 7))

            courses = Course.objects.filter(partner=partner) if partner is not None else Course.objects
            course = courses.get(pk=course_id)

            total_count = Enrollment.objects.exclude(progress=100).filter(course=course).count()
            today = timezone.now() - timedelta(days=days)

            false_starter_count = Enrollment.objects.filter(
                Q(course=course) &
                Q(date_created__lte=timezone.now() - timedelta(days=days)) &
                Q(progress=0)
            ).count()
            false_starter_percentage = false_starter_count / total_count if total_count > 0 else 0

            active_count = 0
            for enrollment in course.enrollments.exclude(progress=100).all():

                event_log = EventLog.objects.filter(user=enrollment.member.user).filter(
                    Q(course=course) |
                    Q(course_material__chapter__course=course)
                ).filter(timestamp__gte=today).first()

                if event_log is not None:
                    active_count += 1
                # end if
            # end for
            active_members_percentage = active_count / total_count if total_count > 0 else 0

            return Response({'false_starter_percentage': false_starter_percentage, 'active_members_percentage': active_members_percentage}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsPartnerOrAdminOnly,))
def member_demographics_view(request):
    '''
    Get member demographics by partner or course
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.filter(user=user).first()

        try:
            course_id = request.query_params.get('course_id', None)
            partner_id = request.query_params.get('partner_id', None)

            members = BaseUser.objects
            if partner is not None:
                members = BaseUser.objects.filter(member__enrollments__course__partner=partner)
            if partner is None and partner_id is not None:
                partner = Partner.objects.get(pk=partner_id)
                members = BaseUser.objects.filter(member__enrollments__course__partner=partner)
            # end if

            course = Course.objects.filter(pk=course_id).first()
            if course is not None:
                members = members.filter(member__enrollments__course=course)
            # end if

            gender = members.values('gender').order_by().annotate(Count('id'))
            location = members.values('location').order_by().annotate(Count('id'))
            age = members.aggregate(Avg('age'))

            return Response({
                'genders': gender,
                'locations': location,
                'average_age': age['age__avg']
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def course_first_enrollment_count_view(request):
    '''
    Get the number of first enrollments in each course
    '''
    if request.method == 'GET':
        try:
            members = Member.objects.all()
            ranking = {}
            days = int(request.query_params.get('days', 999))

            for member in members:
                first_enrollment = member.enrollments.first()

                if first_enrollment is not None and first_enrollment.date_created < timezone.now() - timedelta(days=days):
                    continue
                # end if

                if first_enrollment is not None:
                    course = first_enrollment.course
                    try:
                        ranking[str(course.id)] += 1
                    except KeyError:
                        ranking[str(course.id)] = 1
                # end if
            # end for
            ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
            res = []

            for key in list(ranking.keys())[:10]:
                course = Course.objects.get(pk=key)
                res.append({
                    'course_id': key,
                    'course_title': course.title,
                    'first_enrollment_count': ranking[key],
                })
            # end for

            return Response(res, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Course, Enrollment, Chapter
from .serializers import EnrollmentSerializer, NestedEnrollmentSerializer
from common.models import Member, Partner
from common.permissions import IsMemberOnly


@api_view(['POST', 'DELETE', 'PATCH'])
@permission_classes((IsMemberOnly,))
def course_enrollment_views(request, course_id):
    user = request.user
    '''
    Enrolls a member in a course
    Creates a new Enrollment
    '''
    if request.method == 'POST':
        try:
            member = Member.objects.get(user=user)
            course = Course.objects.get(pk=course_id)

            enrollment = Enrollment.objects.filter(course=course).filter(member=member)
            if enrollment.exists():  # already enrolled
                return Response(status=status.HTTP_409_CONFLICT)
            # end if

            enrollment = Enrollment(progress=0, course=course, member=member)
            enrollment.save()

            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response("Invalid member", status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response("Invalid course", status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Un-enroll member from course
    Deletes course from enrollment object
    '''
    if request.method == 'DELETE':
        try:
            member = Member.objects.get(user=user)
            course = Course.objects.get(pk=course_id)

            enrollment = Enrollment.objects.filter(course=course).get(member=member)
            enrollment.course = None
            enrollment.save()

            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Update member's progress by list of chapters done
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            member = Member.objects.get(user=user)
            course = Course.objects.get(pk=course_id)

            chapters_done = data
            chapters = [str(chapter.id) for chapter in course.chapters.all()]

            total_points = Chapter.objects.filter(course=course).aggregate(Sum('exp_points'))['exp_points__sum']
            curr_points = 0

            for chapter_id in chapters_done:
                # chapter id not found in course
                if chapter_id not in chapters:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                # end if

                chapter = Chapter.objects.get(pk=chapter_id)
                curr_points += float(chapter.exp_points)
            # end for

            # update enrollment
            enrollment = Enrollment.objects.filter(course=course).get(member=member)
            enrollment.chapters_done = chapters_done
            enrollment.progress = curr_points / total_points * 90
            enrollment.save()

            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end def
# end def


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def enrollment_views(request):
    user = request.user
    '''
    Get/Search all enrollments
    '''
    if request.method == 'GET':
        try:
            search = request.query_params.get('search', None)
            course_id = request.query_params.get('courseId', None)

            member = Member.objects.filter(user=user).first()
            partner = Partner.objects.filter(user=user).first()

            enrollments = Enrollment.objects

            if search is not None:
                enrollments = enrollments.filter(
                    Q(course__title__icontains=search) |
                    Q(course__description__icontains=search)
                )
            if course_id is not None:
                enrollments = enrollments.filter(course__id=course_id)
            # end ifs

            if member is not None:
                enrollments = enrollments.filter(member=member)
            elif partner is not None:
                enrollments = enrollments.filter(course__partner=partner)
            # end if-else

            serializer = NestedEnrollmentSerializer(enrollments.all(), many=True, context={'request': request, 'public': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

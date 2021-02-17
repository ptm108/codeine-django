from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Course, Enrollment
from .serializers import EnrollmentSerializer

from common.models import Member
from common.permissions import IsMemberOnly


@api_view(['POST', 'DELETE'])
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
            return Response("Invalid member", status=status.HTTP_404_NOT_FOUND)
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
            return Response("Invalid member", status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from .models import EventLog
from courses.models import Course, CourseMaterial, Quiz
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
            event_log = EventLog(
                payload=data['payload'],
                user=user if user.is_authenticated else None,
                course=course,
                course_material=course_material,
                quiz=quiz,
                industry_project=industry_project,
            )
            event_log.save()
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

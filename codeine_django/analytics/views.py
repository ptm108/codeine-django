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
@permission_classes((AllowAny))
def post_log(request):
    user = request.user
    '''
    Creates a new log
    '''
    if request.method == 'POST':
        data = request.data

        if 'course' in data:
            

        try:
            course = request.query_params.get('course', None)
            event_log = EventLog(
                payload=data['payload'],
                user=user if user.is_authenticated else None,
                course=
            )
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

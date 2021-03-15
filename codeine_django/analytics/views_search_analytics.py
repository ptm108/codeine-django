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

from .models import EventLog


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def course_search_ranking_view(request):
    '''
    Returns top 10 most search terms for courses
    '''
    if request.method == 'GET':
        try:
            event_logs = EventLog.objects.filter(payload='search course')
            period = request.query_params.get('period', None)
            now = timezone.now()

            if period == 'day':
                event_logs = event_logs.filter(timestamp__date=now)
            elif period == 'week':
                week = now.isocalendar()[1]
                event_logs = event_logs.filter(timestamp__week=week)
            elif period == 'month':
                event_logs = event_logs.filter(timestamp__month=now.month)
            elif period == 'year':
                event_logs = event_logs.filter(timestamp__year=now.year)
            # end if-else

            search_ranking = event_logs.values('search_string').order_by().annotate(search_count=Count('id')).order_by('-search_count')
            # print(search_ranking)
            return Response(search_ranking.all()[:10], status=status.HTTP_200_OK)
        except (ValidationError) as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .models import Ticket, TicketMessage
from .serializers import TicketSerializer, TicketMessageSerializer

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def ticket_view(request):
    '''
    Retrieves all tickets
    '''
    if request.method == 'GET':
        tickets = Ticket.objects

        serializer = TicketSerializer(tickets.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# def
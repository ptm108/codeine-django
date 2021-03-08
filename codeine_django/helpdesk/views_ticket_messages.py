from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import Ticket, TicketMessage
from .serializers import TicketMessageSerializer

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def ticket_message_view(request, ticket_id):
    '''
    Retrieves all ticket message for a ticket
    '''
    if request.method == 'GET':
        ticket_messages = TicketMessage.objects.filter(ticket__id=ticket_id)

        # extract query params
        search = request.query_params.get('search', None)

        if search is not None:
            ticket_messages = ticket_messages.filter(
                Q(base_user__user__id__exact=search) |
                Q(message__icontains=search)
            )
        # end if

        serializer = TicketMessageSerializer(ticket_messages.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new ticket message
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data

        with transaction.atomic():
            try:
                ticket = Ticket.objects.get(pk=ticket_id)

                ticket_message = TicketMessage(
                    message = data['message'],
                    base_user = user,
                    ticket = ticket
                )
                ticket_message.save()

                serializer = TicketMessageSerializer(ticket_message)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if
# def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def single_ticket_message_view(request, pk):
    '''
    Get a ticket message by primary key/ id
    '''
    if request.method == 'GET':
        try:
            ticket_message = TicketMessage.objects.get(pk=pk)
            serializer = TicketMessageSerializer(ticket_message)
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
    '''
    Updates message and ticket type
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            with transaction.atomic():
                ticket_message = TicketMessage.objects.get(pk=pk)

                if 'message' in data:
                    ticket_message.message = data['message']

                ticket_message.save()
            # end with

            serializer = TicketMessageSerializer(ticket_message)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TicketMessage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Deletes a ticket
    '''
    if request.method == 'DELETE':
        try:
            ticket_message = TicketMessage.objects.get(pk=pk)
            ticket_message.delete()
            return Response(status=status.HTTP_200_OK)
        except TicketMessage.DoesNotExist:
            return Response('Ticket Message DoesNotExist', status=status.HTTP_400_BAD_REQUEST)
    # end if
# def

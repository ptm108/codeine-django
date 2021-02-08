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
from .models import Ticket
from .serializers import TicketSerializer

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def ticket_view(request):
    '''
    Retrieves all tickets
    '''
    if request.method == 'GET':
        tickets = Ticket.objects

        # extract query params
        search = request.query_params.get('search', None)
        status = request.query_params.get('status', None)

        if search is not None:
            tickets = tickets.filter(
                Q(base_user__user__id__icontains=search) |
                Q(description__icontains=search) |
                Q(ticket_type__icontains=search)
            )
        # end if

        if status is not None:
            tickets = tickets.filter(
                Q(ticket_status__icontains=status)
            )
        # end if


        serializer = TicketSerializer(tickets.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new ticket
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data

        try:
            ticket = Ticket(
                description = data['description'],
                ticket_type = data['ticket_type'],
                base_user = user
            )
            ticket.save()

            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
# def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def single_ticket_view(request, pk):
    '''
    Get a ticket by primary key/ id
    '''
    if request.method == 'GET':
        try:
            ticket = Ticket.objects.get(pk=pk)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
    '''
    Updates description and ticket type
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            ticket = Ticket.objects.get(pk=pk)

            if 'description' in data:
                ticket.description = data['description']
            if 'ticket_type' in data:
                ticket.ticket_type = data['ticket_type']

            ticket.save()
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
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
            ticket = Ticket.objects.get(pk=pk)
            if ticket.ticket_status == 'OPEN':
                ticket.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                # don't allow pending and resolved tickets to be deleted
                return Response('Only OPEN tickets can be deleted', status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response('Ticket DoesNotExist', status=status.HTTP_404_NOT_FOUND)
    # end if
# def

@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def resolve_ticket_view(request, pk):
    '''
    Admin resolves a ticket
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            ticket = Ticket.objects.get(pk=pk)

            ticket.ticket_status = 'RESOLVED'
            ticket.save()

            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

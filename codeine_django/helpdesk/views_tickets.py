from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import Ticket
from .serializers import TicketSerializer
from common.models import BaseUser, PaymentTransaction
from courses.models import Course
from community.models import Article
from industry_projects.models import IndustryProject
from consultations.models import ConsultationSlot


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@parser_classes((MultiPartParser, FormParser))
def ticket_view(request):
    '''
    Retrieves all tickets
    '''
    if request.method == 'GET':
        tickets = Ticket.objects

        # extract query params
        search = request.query_params.get('search', None)
        ticket_status = request.query_params.get('ticket_status', None)

        if search is not None:
            tickets = tickets.filter(
                Q(base_user__user__id__exact=search) |
                Q(description__icontains=search) |
                Q(ticket_type__icontains=search)
            )
        # end if

        if ticket_status is not None:
            tickets = tickets.filter(
                Q(ticket_status__icontains=ticket_status)
            )
        # end if

        serializer = TicketSerializer(tickets.all(), many=True, context={"request": request})
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
                description=data['description'],
                ticket_type=data['ticket_type'],
                base_user=user
            )

            if 'photo' in data:
                ticket.photo = data['photo']
            if 'transaction_id' in data:
                transaction_id = data['transaction_id']
                ticket.transaction = PaymentTransaction.objects.get(pk=transaction_id)
            if 'course_id' in data:
                course_id = data['course_id']
                ticket.course = Course.objects.get(pk=course_id)
            if 'article_id' in data:
                article_id = data['article_id']
                ticket.article = Article.objects.get(pk=article_id)
            if 'industry_project_id' in data:
                industry_project_id = data['industry_project_id']
                ticket.industry_project = IndustryProject.objects.get(pk=industry_project_id)
            if 'consultation_slot_id' in data:
                consultation_slot_id = data['consultation_slot_id']
                ticket.consultation_slot = ConsultationSlot.objects.get(pk=consultation_slot_id)
            # end ifs

            ticket.save()

            serializer = TicketSerializer(ticket, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
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
            return Response(serializer.data, context={"request": request})
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
            # end if

            if 'ticket_type' in data:
                ticket.ticket_type = data['ticket_type']
            # end if

            ticket.save()
            serializer = TicketSerializer(ticket, context={"request": request})
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

            serializer = TicketSerializer(ticket, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

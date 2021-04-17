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
from community.models import Article, CodeReview
from industry_projects.models import IndustryProject
from consultations.models import ConsultationSlot
from notifications.models import Notification, NotificationObject

import json


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
        is_user = request.query_params.get('is_user', None)
        is_assigned_admin = request.query_params.get('is_assigned_admin', None)
        is_assigned = request.query_params.get('is_assigned', None)

        if search is not None:
            tickets = tickets.filter(
                Q(description__icontains=search) |
                Q(ticket_type__icontains=search)
            )
        # end if

        if ticket_status is not None:
            tickets = tickets.filter(
                Q(ticket_status__icontains=ticket_status)
            )
        # end if

        # assumes GET request is made by an user
        # if is_user is None, return all tickets
        # if is_user is True, return all tickets where base_user is request user
        if is_user is not None:
            is_user = json.loads(is_user.lower())
            if is_user is True:
                user = request.user
                tickets = tickets.filter(base_user=user)
            # end if
        # end if

        # assumes GET request is made by an admin
        # if is_assigned_admin is None, return all tickets
        # if is_assigned_admin is True, return all tickets where assigned_admin is request user
        if is_assigned_admin is not None:
            is_assigned_admin = json.loads(is_assigned_admin.lower())
            if is_assigned_admin is True:
                user = request.user
                tickets = tickets.filter(assigned_admin=user)
            # end if
        # end if

        # if is_assigned is None, return all tickets
        # if is_assigned is True, return all assigned tickets
        # if is_assigned is False, return all unassigned tickets
        if is_assigned is not None:
            is_assigned = json.loads(is_assigned.lower())
            if is_assigned is True:
                tickets = tickets.filter(assigned_admin__isnull=False)
            else:
                tickets = tickets.filter(assigned_admin__isnull=True)
            # end if
        # end if

        serializer = TicketSerializer(
            tickets.all(), many=True, context={"request": request})
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
                ticket.transaction = PaymentTransaction.objects.get(
                    pk=transaction_id)
            if 'course_id' in data:
                course_id = data['course_id']
                ticket.course = Course.objects.get(pk=course_id)
            if 'article_id' in data:
                article_id = data['article_id']
                ticket.article = Article.objects.get(pk=article_id)
            if 'industry_project_id' in data:
                industry_project_id = data['industry_project_id']
                ticket.industry_project = IndustryProject.objects.get(
                    pk=industry_project_id)
            if 'consultation_slot_id' in data:
                consultation_slot_id = data['consultation_slot_id']
                ticket.consultation_slot = ConsultationSlot.objects.get(
                    pk=consultation_slot_id)
            if 'code_review_id' in data:
                code_review_id = data['code_review_id']
                ticket.code_review = CodeReview.objects.get(pk=code_review_id)
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
            serializer = TicketSerializer(ticket, context={"request": request})
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

    # '''
    # Updates description and ticket type
    # '''
    # if request.method == 'PUT':
    #     data = request.data
    #     try:
    #         ticket = Ticket.objects.get(pk=pk)

    #         if 'description' in data:
    #             ticket.description = data['description']
    #         # end if

    #         if 'ticket_type' in data:
    #             ticket.ticket_type = data['ticket_type']
    #         # end if

    #         ticket.save()
    #         serializer = TicketSerializer(ticket, context={"request": request})
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Ticket.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except (KeyError, ValueError) as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     # end try-except
    # # end if

    '''
    Deletes a ticket
    '''
    if request.method == 'DELETE':
        try:
            ticket = Ticket.objects.get(pk=pk)
            if ticket.ticket_status == 'OPEN':
                user = request.user
                if ticket.base_user != user:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                # end if

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

            # notify user
            title = f'Helpdesk: Ticket has been resolved!'
            description = f'Ticket has been marked as resolved by the Codeine admin team! Feel free to contact us if you have any further questions.'
            notification_type = 'HELPDESK'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, ticket=ticket)
            notification.save()

            receiver = ticket.base_user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()

            serializer = TicketSerializer(ticket, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def open_ticket_view(request, pk):
    '''
    Admin open a ticket
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            ticket = Ticket.objects.get(pk=pk)

            ticket.ticket_status = 'OPEN'
            ticket.save()

            # notify user
            title = f'Helpdesk: Ticket has been opened!'
            description = f'Ticket has been marked as opened by the Codeine admin team!'
            notification_type = 'HELPDESK'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, ticket=ticket)
            notification.save()

            receiver = ticket.base_user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()

            serializer = TicketSerializer(ticket, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def assign_ticket_view(request, pk):
    '''
    Admin assigns a ticket
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            if 'admin_id' in data:
                ticket = Ticket.objects.get(pk=pk)
                admin_id = data['admin_id']

                admin = BaseUser.objects.get(pk=admin_id)

                if admin.is_admin is False:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                # end if

                ticket.assigned_admin = admin
                ticket.save()

                # notify assigned admin
                title = f'Helpdesk: A new ticket has been assigned to you!'
                description = f'Ticket {ticket.description}'
                notification_type = 'HELPDESK'
                notification = Notification(
                    title=title, description=description, notification_type=notification_type, ticket=ticket)
                notification.save()

                notification_object = NotificationObject(
                    receiver=admin, notification=notification)
                notification_object.save()

                serializer = TicketSerializer(
                    ticket, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if-else
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def unassign_ticket_view(request, pk):
    '''
    Admin unassigns a ticket
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            ticket = Ticket.objects.get(pk=pk)
            prev_admin = ticket.assigned_admin
            ticket.assigned_admin = None
            ticket.save()

            # notify unassigned admin
            title = f'Helpdesk: A new ticket has been unassigned from you!'
            description = f'Ticket {ticket.description}'
            notification_type = 'HELPDESK'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, ticket=ticket)
            notification.save()

            notification_object = NotificationObject(
                receiver=prev_admin, notification=notification)
            notification_object.save()

            serializer = TicketSerializer(
                ticket, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

from django.shortcuts import render
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from common.models import Member, Organization, Partner
from common.permissions import IsMemberOrReadOnly, IsMemberOnly, IsPartnerOnly
from .models import Event, EventApplication
from .serializers import EventApplicationSerializer

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def event_application_view(request, event_id):
    '''
    Creates a new event application
    '''
    if request.method == 'POST':
        user = request.user
        member = Member.objects.get(user=user)
        data = request.data

        event = Event.objects.get(pk=event_id)

        # check if event is cancelled
        if event.is_cancelled is True:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end if            

        prev_applications = EventApplication.objects.filter(
            Q(event=event) &
            Q(is_cancelled=False)
        )

        # check if event already has maxed out the number of vacancies
        if prev_applications.count() >= event.max_members:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end if

        prev_applications = prev_applications.filter(
            Q(member=member)
        )

        # check if member has already has a non-cancelled slot
        if prev_applications.count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end if

        with transaction.atomic():
            try:
                event_application = EventApplication(
                    member=member,
                    event=event
                )

                event_application.save()

                serializer = EventApplicationSerializer(
                    event_application, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get event applications for this event 
    '''
    if request.method == 'GET':
        # extract query params
        member_id = request.query_params.get('member_id', None)

        event = Event.objects.get(pk=event_id)
        event_applications = EventApplication.objects.filter(event=event)
        
        if member_id is not None:
            event_applications = event_applications.filter(
                Q(member__user__id__exact=member_id)
            )
        # end if

        serializer = EventApplicationSerializer(
            event_applications.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

@api_view(['GET'])
@permission_classes((IsMemberOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_event_application_view(request, pk):
    '''
    Gets an event application by primary key/ id
    '''
    if request.method == 'GET':
        try:
            event_application = EventApplication.objects.get(pk=pk)

            return Response(EventApplicationSerializer(event_application, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
#end def

@api_view(['PATCH'])
@permission_classes((IsMemberOnly,))
def cancel_event_application(request, pk):
    '''
    Member cancels an event appplication
    '''
    if request.method == 'PATCH':
        try:
            event_application = EventApplication.objects.get(pk=pk)

            user = request.user
            member = event_application.member

            # assert requesting member is cancelling their own event application
            if member.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            # assert that slot is not already cancelled or rejected
            if event_application.is_cancelled or event_application.is_rejected:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            event_application.is_cancelled = True
            event_application.save()

            serializer = EventApplicationSerializer(
                event_application, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

@api_view(['GET'])
@permission_classes((IsPartnerOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def partner_event_application_view(request):
    '''
    Partner Get/ Search event applications
    '''
    if request.method == 'GET':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)
            organization = partner.organization
            if organization is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            events = Event.objects.filter(organization=organization)
            event_applications = EventApplication.objects.filter(event__in=events)
            
            search = request.query_params.get('search', None)
            if search is not None:
                event_applications = event_applications.filter(
                    Q(event__title__icontains=search) |
                    Q(member__user__first_name__icontains=search) |
                    Q(member__user__last_name__icontains=search)
                )
            # end if

            serializer = EventApplicationSerializer(
                event_applications.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
#end def

@api_view(['GET'])
@permission_classes((IsMemberOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def member_event_application_view(request):
    '''
    Member Get/ Search event applications
    '''
    if request.method == 'GET':
        try:
            user = request.user
            member = Member.objects.get(user=user)
            event_applications = EventApplication.objects.filter(member=member)
            
            search = request.query_params.get('search', None)
            if search is not None:
                event_applications = event_applications.filter(
                    Q(event__title__icontains=search)
                )
            # end if

            serializer = EventApplicationSerializer(
                event_applications.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
#end def

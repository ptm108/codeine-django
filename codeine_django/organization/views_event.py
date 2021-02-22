from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from common.models import Partner, Organization
from common.permissions import IsPartnerOnly, IsPartnerOrReadOnly
from .models import Event, EventApplication
from .serializers import EventSerializer

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsPartnerOrReadOnly,))
def event_view(request):
    '''
    Creates a new event
    '''
    if request.method == 'POST':
        data = request.data
        user = request.user
        partner = Partner.objects.get(user=user)
        organization = partner.organization

        if organization is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end if

        with transaction.atomic():
            try:
                event = Event(
                    title = data['title'],
                    start_time = data['start_time'],
                    end_time = data['end_time'],
                    meeting_link = data['meeting_link'],
                    price_per_pax = data['price_per_pax'],
                    max_members = data['max_members'],
                    organization = organization
                )

                event.save()

                serializer = EventSerializer(event, context={"request": request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get all events
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)
        organization_id = request.query_params.get('organization_id', None)
        is_cancelled = request.query_params.get('is_cancelled', None)

        events = Event.objects

        if search is not None:
            events = events.filter(
                Q(title__icontains=search) |
                Q(organization__organization_name__icontains=search)
            )
        # end if

        if organization_id is not None:
            events = events.filter(
                Q(organization__id=organization_id)
            )
        # end if

        if is_cancelled is not None:
            events = events.filter(
                Q(is_cancelled=is_cancelled)
            )
        # end if

        serializer = EventSerializer(
            events.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsPartnerOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_event_view(request, pk):
    '''
    Gets an event by primary key/ id
    '''
    if request.method == 'GET':
        try:
            event = Event.objects.get(pk=pk)
            return Response(EventSerializer(event, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

    '''
    Updates start time, end time and meeting link for Event
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            with transaction.atomic():
                event = Event.objects.get(pk=pk)
                organization = event.organization
                
                user =  request.user
                partner = Partner.objects.get(user=user)                

                if partner.organization is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                # end if

                # assert requesting partner is confirming their organization's event
                if partner.organization != organization:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                # end if

                if 'title' in data:
                    event.title = data['title']
                if 'start_date' in data:
                    event.start_date = data['start_date']
                if 'end_date' in data:
                    event.end_date = data['end_date']
                if 'start_time' in data:
                    event.start_time = data['start_time']
                if 'end_time' in data:
                    event.end_time = data['end_time']
                if 'meeting_link' in data:
                    event.meeting_link = data['meeting_link']
                if 'price_per_pax' in data:
                    event.price_per_pax = data['price_per_pax']
                if 'max_members' in data:
                    event.max_members = data['max_members']

                event.save()
            # end with

            serializer = EventSerializer(event, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def cancel_event(request, pk):
    '''
    Partner cancels event
    '''
    if request.method == 'PATCH':
        try:
            event = Event.objects.get(pk=pk)
            organization = event.organization
                
            user =  request.user
            partner = Partner.objects.get(user=user)                

            if partner.organization is None:
               return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            # assert requesting partner is confirming their organization's event
            if partner.organization != organization:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            # assert requesting partner is rejecting their own event
            if partner.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            event.is_cancelled = True
            event.save()

            # reject all event applications
            event_applications = EventApplication.objects.filter(event=event)
            for application in event_applications:
                application.is_rejected = True
                application.save()
            # end for

            serializer = EventSerializer(event, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import ConsultationSlot
from .serializers import ConsultationSlotSerializer
from datetime import datetime, timedelta


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def consultation_slot_view(request):
    '''
    Creates a new consultation slot
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data

        # if (datetime.strptime(data['end_time']) > datetime.strptime(data['start_time'])):
        #     return Response({'message': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                consultation_slot = ConsultationSlotSerializer(
                    start_date = data['start_date'],
                    end_date = data['end_date'],
                    start_time = data['start_time'],
                    end_time = data['end_time'],
                    meeting_link = data['meeting_link'],
                    content_provider = user
                )
                consultation_slot.save()

                serializer = ConsultationSlotSerializer(
                    consultation_slot, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if

    '''
    Get all consultation slots
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        consultation_slots = ConsultationSlot.objects

        if search is not None:
            consultation_slots = consultation_slots.filter(
                Q(content_provider__user__id__contains=search) |
                Q(member__user__id__contains=search)
            )
        # end if

        serializer = ConsultationSlotSerializer(
            consultation_slots.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
@parser_classes((MultiPartParser, FormParser,))
def single_consultation_slot_view(request, pk):
    '''
    Gets a consultation slot by primary key/ id
    '''
    if request.method == 'GET':
        try:
            consultation_slot = ConsultationSlot.objects.get(pk=pk)

            return Response(ConsultationSlotSerializer(consultation_slot, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

    '''
    Updates start time, end time and meeting link for Consultation Slot
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            with transaction.atomic():
                consultation_slot = ConsultationSlot.objects.get(pk=pk)

                if 'start_date' in data:
                    consultation_slot.start_date = data['start_date']
                if 'end_date' in data:
                    consultation_slot.end_date = data['end_date']
                if 'start_time' in data:
                    consultation_slot.start_time = data['start_time']
                if 'end_time' in data:
                    consultation_slot.end_time = data['end_time']
                if 'meeting_link' in data:
                    consultation_slot.meeting_link = data['meeting_link']
                consultation_slot.save()
            # end with

            serializer = ConsultationSlotSerializer(consultation_slot, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConsultationSlot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a consultation slot
    '''
    if request.method == 'DELETE':
        try:
            consultation_slot = ConsultationSlot.objects.get(pk=pk)
            if consultation_slot.is_confirmed is True:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                consultation_slot.delete()
                return Response(status=status.HTTP_200_OK)
        except ConsultationSlot.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def confirm_consultation_slot(request, pk):
    '''
    Content Provider confirms a consultation slot
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            consultation_slot = ConsultationSlot.objects.get(pk=pk)

            user = request.user
            content_provider = consultation_slot.content_provider

            # assert requesting content provider is confirming their own consultation slots
            if content_provider.user != user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            consultation_slot.is_confirmed = True
            consultation_slot.save()

            serializer = ConsultationSlotSerializer(
                consultation_slot, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def reject_consultation_slot(request, pk):
    '''
    Content Provider rejects a consultation slot
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            consultation_slot = ConsultationSlot.objects.get(pk=pk)

            user = request.user
            content_provider = consultation_slot.content_provider

            # assert requesting content provider is rejecting their own consultation slots
            if content_provider.user != user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            consultation_slot.is_rejected = True
            consultation_slot.save()

            serializer = ConsultationSlotSerializer(
                consultation_slot, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

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
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import ConsultationSlot
from common.models import Partner, Member
from common.permissions import IsMemberOnly, IsPartnerOnly, IsPartnerOrReadOnly
from .serializers import ConsultationSlotSerializer
from datetime import datetime, timedelta


@api_view(['GET', 'POST'])
@permission_classes((IsPartnerOrReadOnly,))
def consultation_slot_view(request):
    '''
    Creates a new consultation slot
    '''
    if request.method == 'POST':
        user = request.user
        partner = Partner.objects.get(user=user)
        data = request.data

        # if (datetime.strptime(data['end_time']) > datetime.strptime(data['start_time'])):
        #     return Response({'message': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                consultation_slot = ConsultationSlot(
                    # start_date = data['start_date'],
                    # end_date = data['end_date'],
                    title = data['title'],
                    start_time = data['start_time'],
                    end_time = data['end_time'],
                    meeting_link = data['meeting_link'],
                    price_per_pax = data['price_per_pax'],
                    max_members = data['max_members'],
                    r_rule = data['r_rule'],
                    is_all_day = data['is_all_day'],
                    partner = partner
                )

                consultation_slot.save()

                serializer = ConsultationSlotSerializer(
                    consultation_slot, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get all consultation slots
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)
        partner_id = request.query_params.get('partner_id', None)

        consultation_slots = ConsultationSlot.objects

        if search is not None:
            consultation_slots = consultation_slots.filter(
                Q(title__icontains=search)
            )
        # end if

        if partner_id is not None:
            consultation_slots = consultation_slots.filter(
                Q(partner__user__id__exact=partner_id)
            )
        # end if

        serializer = ConsultationSlotSerializer(
            consultation_slots.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsPartnerOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
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
                partner = consultation_slot.partner
                user =  request.user
                # assert requesting partner is confirming their own consultation slots
                if partner.user != user:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                # end if

                if 'title' in data:
                    consultation_slot.title = data['title']
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
                if 'price_per_pax' in data:
                    consultation_slot.price_per_pax = data['price_per_pax']
                if 'max_members' in data:
                    consultation_slot.max_members = data['max_members']
                if 'r_rule' in data:
                    consultation_slot.r_rule = data['r_rule']
                if 'is_all_day' in data:
                    consultation_slot.is_all_day = data['is_all_day']

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
# end def

@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def cancel_consultation_slot(request, pk):
    '''
    Partner cancels consultation slot
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            consultation_slot = ConsultationSlot.objects.get(pk=pk)

            user = request.user
            partner = consultation_slot.partner

            # assert requesting partner is rejecting their own consultation slots
            if partner.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            consultation_slot.is_cancelled = True
            consultation_slot.save()

            serializer = ConsultationSlotSerializer(
                consultation_slot, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

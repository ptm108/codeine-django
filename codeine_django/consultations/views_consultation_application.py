from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from .models import ConsultationApplication, ConsultationSlot
from common.models import Member, Partner
from common.permissions import IsMemberOnly, IsMemberOrReadOnly, IsPartnerOnly
from .serializers import ConsultationApplicationSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def consultation_application_view(request, consultation_slot_id):
    '''
    Creates a new consultation application
    '''
    if request.method == 'POST':
        user = request.user
        member = Member.objects.get(user=user)
        data = request.data

        consultation_slot = ConsultationSlot.objects.get(pk=consultation_slot_id)

        # check if consultation is cancelled
        if consultation_slot.is_cancelled is True:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end if            

        prev_applications = ConsultationApplication.objects.filter(
            Q(consultation_slot=consultation_slot) &
            Q(is_cancelled=False)
        )

        # check if consultation already has maxed out the number of slots
        if prev_applications.count() >= consultation_slot.max_members:
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
                consultation_application = ConsultationApplication(
                    member=member,
                    consultation_slot=consultation_slot
                )

                consultation_application.save()

                serializer = ConsultationApplicationSerializer(
                    consultation_application, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get consultation applications for this consultation slot
    '''
    if request.method == 'GET':
        # extract query params
        member_id = request.query_params.get('member_id', None)

        consultation_slot = ConsultationSlot.objects.get(pk=consultation_slot_id)
        consultation_applications = ConsultationApplication.objects.filter(consultation_slot=consultation_slot)
        
        if member_id is not None:
            consultation_applications = consultation_applications.filter(
                Q(member__user__id__exact=member_id)
            )
        # end if

        serializer = ConsultationApplicationSerializer(
            consultation_applications.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsMemberOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_consultation_application_view(request, pk):
    '''
    Gets a consultation application by primary key/ id
    '''
    if request.method == 'GET':
        try:
            consultation_application = ConsultationApplication.objects.get(pk=pk)

            return Response(ConsultationApplicationSerializer(consultation_application, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
#end def

@api_view(['PATCH'])
@permission_classes((IsMemberOnly,))
def cancel_consultation_application(request, pk):
    '''
    Member cancels a consultation appplication
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            consultation_application = ConsultationApplication.objects.get(pk=pk)

            user = request.user
            member = consultation_application.member

            # assert requesting member is cancelling their own consultation slots
            if member.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            # assert that slot is not already cancelled or rejected
            if consultation_application.is_cancelled or consultation_application.is_rejected:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            consultation_application.is_cancelled = True
            consultation_application.save()

            serializer = ConsultationApplicationSerializer(
                consultation_application, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

@api_view(['GET'])
@permission_classes((IsPartnerOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def partner_consultation_application_view(request):
    '''
    Partner Get/ Search consultation applications
    '''
    if request.method == 'GET':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)
            consultation_slots = ConsultationSlot.objects.filter(partner=partner)
            consultation_applications = ConsultationApplication.objects.filter(consultation_slot__in=consultation_slots)
            
            search = request.query_params.get('search', None)
            if search is not None:
                consultation_applications = consultation_applications.filter(
                    Q(consultation_slot__title__icontains=search) |
                    Q(member__user__first_name__icontains=search) |
                    Q(member__user__last_name__icontains=search)
                )
            # end if

            serializer = ConsultationApplicationSerializer(
                consultation_applications.all(), many=True, context={"request": request})
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
def member_consultation_application_view(request):
    '''
    Member Get/ Search consultation applications
    '''
    if request.method == 'GET':
        try:
            user = request.user
            member = Member.objects.get(user=user)
            consultation_applications = ConsultationApplication.objects.filter(member=member)
            
            search = request.query_params.get('search', None)
            if search is not None:
                consultation_applications = consultation_applications.filter(
                    Q(consultation_slot__title__icontains=search)
                )
            # end if

            serializer = ConsultationApplicationSerializer(
                consultation_applications.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
#end def

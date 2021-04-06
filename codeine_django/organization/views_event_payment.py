from django.shortcuts import render
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from common.models import Member, PaymentTransaction
from common.permissions import IsMemberOrReadOnly, IsMemberOrAdminOrReadOnly
from .models import EventPayment, EventApplication
from .serializers import EventPaymentSerializer

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def event_payment_view(request, event_application_id):
    '''
    Creates a new payment transaction for an event application
    '''
    if request.method == 'POST':
        user = request.user
        member = Member.objects.get(user=user)
        event_application = EventApplication.objects.get(pk=event_application_id)
        data = request.data

        # assert requesting member is paying for their own slot
        if member != event_application.member:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # end if

        prev_payments = EventPayment.objects.filter(
            Q(event_application=event_application) &
            (Q(payment_transaction__payment_status='PENDING_COMPLETION') |
             Q(payment_transaction__payment_status='COMPLETED'))
        )

        # check if application already has a payment, and is not failed
        if prev_payments.count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end if

        with transaction.atomic():
            try:
                payment_transaction = PaymentTransaction(
                    payment_amount=data['payment_amount'],
                    payment_type=data['payment_type']
                )
                payment_transaction.save()

                event_payment = EventPayment(
                    payment_transaction=payment_transaction,
                    event_application=event_application
                )
                event_payment.save()

                serializer = EventPaymentSerializer(
                    event_payment, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get event payments for an event application
    '''
    if request.method == 'GET':
        # extract query params
        event_application = EventApplication.objects.get(pk=event_application_id)

        event_payments = EventPayment.objects.filter(event_application=event_application)

        serializer = EventPaymentSerializer(
            event_payments.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsMemberOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_event_payment_view(request, pk):
    '''
    Gets an event payment by primary key/ id
    '''
    if request.method == 'GET':
        try:
            event_payment = EventPayment.objects.get(pk=pk)

            return Response(EventPaymentSerializer(event_payment, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsMemberOrAdminOrReadOnly,))
def update_event_payment_status(request, pk):
    '''
    Update event payment status
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            event_payment = EventPayment.objects.get(pk=pk)

            if 'payment_status' in data:
                event_payment.payment_transaction.payment_status = data['payment_status']
            # end if
            event_payment.payment_transaction.save()
            event_payment.save()

            serializer = EventPaymentSerializer(
                event_payment, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

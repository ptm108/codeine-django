from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from common.models import Member
from common.permissions import IsMemberOrReadOnly, IsMemberOrAdminOrReadOnly
from .models import PaymentTransaction, ConsultationSlot
from .serializers import PaymentTransactionSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def consultation_payment_view(request, pk):
    '''
    Creates a new payment transaction for a consultation
    '''
    if request.method == 'POST':
        user = request.user
        member = Member.objects.get(user=user)
        consultation_slot = ConsultationSlot.objects.get(id=pk)
        partner = consultation_slot.partner
        data = request.data

        with transaction.atomic():
            try:
                payment_transaction = ConsultationSlot(
                    payment_amount = data['payment_amount'],
                    payment_status = data['payment_status'],
                    payment_type = data['payment_type'],
                    consultation_slot = consultation_slot,
                    partner = partner
                )

                payment_transaction.save()

                serializer = PaymentTransactionSerializer(
                    payment_transaction, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if

    '''
    Get all payment transactions
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        payment_transactions = PaymentTransaction.objects

        if search is not None:
            payment_transactions = payment_transactions.filter(
                Q(payment_amount__icontains=search) |
                Q(payment_status__icontains=search) |
                Q(payment_type__icontains=search) |
                Q(consultation_slot_id__icontains=search) |
                Q(partner_id__icontains=search)
            )
        # end if

        serializer = PaymentTransactionSerializer(
            payment_transactions.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def payment_transaction_view(request, consultation_slot_id):
    '''
    Creates a new payment transaction
    '''
    if request.method == 'POST':
        user = request.user
        member = Member.objects.get(user=user)
        consultation_slot = ConsultationSlot.objects.get(id=consultation_slot_id)
        partner = consultation_slot.partner
        data = request.data

        with transaction.atomic():
            try:
                payment_transaction = ConsultationSlot(
                    payment_amount = data['payment_amount'],
                    payment_status = data['payment_status'],
                    payment_type = data['payment_type'],
                    consultation_slot = consultation_slot,
                    partner = partner
                )

                payment_transaction.save()

                serializer = PaymentTransactionSerializer(
                    payment_transaction, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if

    '''
    Get all payment transactions
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        payment_transactions = PaymentTransaction.objects

        if search is not None:
            payment_transactions = payment_transactions.filter(
                Q(payment_amount__icontains=search) |
                Q(payment_status__icontains=search) |
                Q(payment_type__icontains=search) |
                Q(consultation_slot_id__icontains=search) |
                Q(partner_id__icontains=search)
            )
        # end if

        serializer = PaymentTransactionSerializer(
            payment_transactions.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsMemberOrAdminOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_payment_transaction_view(request, pk):
    '''
    Gets a payment transaction by primary key/ id
    '''
    if request.method == 'GET':
        try:
            payment_transaction = PaymentTransaction.objects.get(pk=pk)

            return Response(PaymentTransactionSerializer(payment_transaction, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

    '''
    Updates payment_amount, payment_status and payment_type for Payment Transaction
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            with transaction.atomic():
                payment_transaction = PaymentTransaction.objects.get(pk=pk)

                if 'payment_amount' in data:
                    payment_transaction.payment_amount = data['payment_amount']
                if 'payment_status' in data:
                    payment_transaction.payment_status = data['payment_status']
                if 'payment_type' in data:
                    payment_transaction.payment_type = data['payment_type']

                payment_transaction.save()
            # end with

            serializer = PaymentTransactionSerializer(payment_transaction, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaymentTransaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a payment transaction
    '''
    if request.method == 'DELETE':
        try:
            payment_transaction = PaymentTransaction.objects.get(pk=pk)
            payment_transaction.delete()
            return Response(status=status.HTTP_200_OK)
        except PaymentTransaction.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
# end def

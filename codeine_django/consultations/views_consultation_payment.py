from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from common.models import PaymentTransaction, Member, Partner
from common.permissions import IsMemberOnly, IsMemberOrReadOnly, IsMemberOrAdminOrReadOnly, IsPartnerOnly, IsMemberOrPartnerOrReadOnly
from .models import ConsultationPayment, ConsultationApplication, ConsultationSlot
from .serializers import ConsultationPaymentSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def consultation_payment_view(request, consultation_application_id):
    '''
    Creates a new payment transaction for a consultation
    '''
    if request.method == 'POST':
        user = request.user
        member = Member.objects.get(user=user)
        consultation_application = ConsultationApplication.objects.get(pk=consultation_application_id)
        data = request.data

        # assert requesting member is paying for their own slot
        if member != consultation_application.member:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # end if

        prev_payments = ConsultationPayment.objects.filter(
            Q(consultation_application=consultation_application) &
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
                    payment_amount = data['payment_amount'],
                    payment_type = data['payment_type'],
                    payment_status='COMPLETED'
                )
                payment_transaction.save()

                consultation_payment = ConsultationPayment(
                    payment_transaction = payment_transaction,
                    consultation_application = consultation_application
                )
                consultation_payment.save()

                serializer = ConsultationPaymentSerializer(
                    consultation_payment, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get consultation payments for a consultation application
    '''
    if request.method == 'GET':
        # extract query params
        consultation_application = ConsultationApplication.objects.get(pk=consultation_application_id)

        consultation_payments = ConsultationPayment.objects.filter(consultation_application=consultation_application)

        serializer = ConsultationPaymentSerializer(
            consultation_payments.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

@api_view(['GET'])
@permission_classes((IsMemberOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_consultation_payment_view(request, pk):
    '''
    Gets a consultation payment by primary key/ id
    '''
    if request.method == 'GET':
        try:
            consultation_payment = ConsultationPayment.objects.get(pk=pk)

            return Response(ConsultationPaymentSerializer(consultation_payment, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
#end def

@api_view(['PATCH'])
@permission_classes((IsMemberOrAdminOrReadOnly,))
def update_consultation_payment_status(request, pk):
    '''
    Update consultation payment status
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            consultation_payment = ConsultationPayment.objects.get(pk=pk)

            if 'payment_status' in data:
                consultation_payment.payment_transaction.payment_status = data['payment_status']
            # end if
            consultation_payment.payment_transaction.save()
            consultation_payment.save()

            serializer = ConsultationPaymentSerializer(
                consultation_payment, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

@api_view(['POST'])
@permission_classes((IsMemberOrPartnerOrReadOnly,))
def refund_consultation_payment_status(request, pk):
    '''
    Refund consultation payment
    '''
    if request.method == 'POST':
        data = request.data
        
        with transaction.atomic():
            try:
                previous_consultation_payment = ConsultationPayment.objects.get(pk=pk)

                payment_transaction = PaymentTransaction(
                    payment_amount = previous_consultation_payment.payment_transaction.payment_amount,
                    payment_type = previous_consultation_payment.payment_transaction.payment_type,
                    payment_status='REFUNDED'
                )
                payment_transaction.save()

                consultation_payment = ConsultationPayment(
                    payment_transaction = payment_transaction,
                    consultation_application = previous_consultation_payment.consultation_application
                )
                consultation_payment.save()

                serializer = ConsultationPaymentSerializer(
                    consultation_payment, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if
# end def

@api_view(['GET'])
@permission_classes((IsPartnerOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def partner_consultation_payment_view(request):
    '''
    Partner Get/ Search consultation payment transactions
    '''
    if request.method == 'GET':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)
            consultation_slots = ConsultationSlot.objects.filter(partner=partner)
            consultation_applications = ConsultationApplication.objects.filter(consultation_slot__in=consultation_slots)
            consultation_payments = ConsultationPayment.objects.filter(consultation_application__in=consultation_applications)

            serializer = ConsultationPaymentSerializer(
                consultation_payments.all(), many=True, context={"request": request})
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
def member_consultation_payment_view(request):
    '''
    Member Get/ Search consultation payment transactions
    '''
    if request.method == 'GET':
        try:
            user = request.user
            member = Member.objects.get(user=user)
            consultation_applications = ConsultationApplication.objects.filter(member=member)
            consultation_payments = ConsultationPayment.objects.filter(consultation_application__in=consultation_applications)

            serializer = ConsultationPaymentSerializer(
                consultation_payments.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
#end def
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from common.models import Member
from common.permissions import IsMemberOrReadOnly
from .models import PaymentTransaction, ConsultationPayment, ConsultationApplication
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

        with transaction.atomic():
            try:
                payment_transaction = PaymentTransaction(
                    payment_amount = data['payment_amount'],
                    payment_type = data['payment_type']
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
    Get consultation payment for a consultation application
    '''
    if request.method == 'GET':
        # extract query params
        consultation_application = ConsultationApplication.objects.get(pk=consultation_application_id)

        consultation_payment = ConsultationPayment.objects.filter(consultation_application=consultation_application)

        serializer = ConsultationPaymentSerializer(
            consultation_payment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

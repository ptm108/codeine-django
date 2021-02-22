from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from common.models import PaymentTransaction, Partner, Organization
from common.permissions import IsPartnerOnly
from .models import ContributionPayment
from .serializers import ContributionPaymentSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsPartnerOnly,))
def contribution_payment_view(request):
    '''
    Creates a new payment transaction for a contribution
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
                payment_transaction = PaymentTransaction(
                    payment_amount = data['payment_amount'],
                    payment_type = data['payment_type']
                )
                payment_transaction.save()

                contribution_payment = ContributionPayment(
                    payment_transaction = payment_transaction,
                    organization = organization,
                    made_by = partner
                )
                contribution_payment.save()

                serializer = ContributionPaymentSerializer(
                    contribution_payment, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get contribution payments for the partner's organization
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.get(user=user)
        organization = partner.organization

        if organization is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end if

        contribution_payments = ContributionPayment.objects.filter(organization=organization)

        serializer = ContributionPaymentSerializer(
            contribution_payments.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

@api_view(['GET'])
@permission_classes((IsPartnerOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_contribution_payment_view(request, pk):
    '''
    Gets a contribution payment by primary key/ id
    '''
    if request.method == 'GET':
        try:
            contribution_payment = ContributionPayment.objects.get(pk=pk)
            return Response(ContributionPaymentSerializer(contribution_payment, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
#end def

@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def update_contribution_payment_view(request, pk):
    '''
    Update contribution payment status
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            contribution_payment = ContributionPayment.objects.get(pk=pk)

            if 'payment_status' in data:
                contribution_payment.payment_transaction.payment_status = data['payment_status']
            # end if
            contribution_payment.payment_transaction.save()
            contribution_payment.save()

            serializer = ContributionPaymentSerializer(
                contribution_payment, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

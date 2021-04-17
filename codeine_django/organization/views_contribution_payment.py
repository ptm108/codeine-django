from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from datetime import datetime

from .models import ContributionPayment
from .serializers import ContributionPaymentSerializer
from common.models import PaymentTransaction, Partner, Organization
from common.permissions import IsPartnerOnly


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

        with transaction.atomic():
            try:
                # check if there is a pending completion
                if ContributionPayment.objects.filter(payment_transaction__payment_status='PENDING_COMPLETION'):
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                # end if

                payment_transaction = PaymentTransaction(
                    payment_amount=float(data['contribution']),
                    payment_type=data['payment_type']
                )
                payment_transaction.save()

                # # get today's date or last contribution expiry date
                # month_duration = int(data['month_duration'])
                # now = datetime.now()
                # contribution = ContributionPayment.objects.filter(Q(made_by=partner) | Q(organization=organization)).first()

                # if contribution is not None:
                #     now = contribution.expiry_date
                #     month_duration -= 1
                # # end if

                # year = now.year
                # month = now.month + month_duration + 1  # first of the next month

                # if month > 12:
                #     month = month % 12 + 1
                #     year += 1
                # # end if

                # expiry_date = timezone.make_aware(datetime(year, month, 1))

                contribution_payment = ContributionPayment(
                    payment_transaction=payment_transaction,
                    organization=organization,
                    made_by=partner,
                )
                contribution_payment.save()

                serializer = ContributionPaymentSerializer(contribution_payment, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get contribution payments for the partner or organization
    '''
    if request.method == 'GET':
        user = request.user
        partner = Partner.objects.get(user=user)
        organization = partner.organization

        contribution_payments = ContributionPayment.objects
        # if organization is null, return contributions made by that partner
        if organization is None:
            contribution_payments = contribution_payments.filter(made_by=partner)
        else:  # organization is not null, return contributions made by the organization
            contribution_payments = contribution_payments.filter(organization=organization)
        # end if-else

        latest = request.query_params.get('latest', None)
        payment_status = request.query_params.get('payment_status', None)

        # contribution_payments = ContributionPayment.objects.filter(Q(made_by=partner) | Q(organization=organization))

        if payment_status is not None:
            contribution_payments = contribution_payments.filter(payment_transaction__payment_status=payment_status)
        if latest is not None:
            return Response(ContributionPaymentSerializer(contribution_payments.order_by('-timestamp').first(), context={"request": request}).data, status=status.HTTP_200_OK)
        # end if

        serializer = ContributionPaymentSerializer(contribution_payments.all(), context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@ api_view(['GET', 'DELETE'])
@ permission_classes((IsPartnerOnly,))
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
        # end try-except
    # end if

    '''
    Deletes a contribution payment by id
    '''
    if request.method == 'DELETE':
        try:
            contribution_payment = ContributionPayment.objects.get(pk=pk)
            if contribution_payment.payment_transaction.payment_status != 'PENDING_COMPLETION':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if
            contribution_payment.delete()

            return Response(ContributionPaymentSerializer(contribution_payment, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@ api_view(['PATCH'])
@ permission_classes((IsPartnerOnly,))
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

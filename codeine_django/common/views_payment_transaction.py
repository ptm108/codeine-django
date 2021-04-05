from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsAdminOnly
from .models import PaymentTransaction
from notifications.serializers import PaymentTransactionSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def payment_transaction_view(request):
    '''
    Get all payment transactions
    '''
    if request.method == 'GET':
        payment_transactions = PaymentTransaction.objects
        serializer = PaymentTransactionSerializer(payment_transactions.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def single_payment_transaction_view(request, pk):
    '''
    Delete payment transaction
    '''
    if request.method == 'DELETE':
        try:
            payment_transaction = PaymentTransaction.objects.get(pk=pk)
            if payment_transaction.payment_status != 'PENDING_COMPLETION':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            if payment_transaction.membership_subscription:
                member = payment_transaction.membership_subscription.member

                # assert requesting member is getting their own Membership Subscription
                if member.user != request.user:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                # end if

                payment_transaction.membership_subscription.delete()
                payment_transaction.delete()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .permissions import IsAdminOnly
from .models import PaymentTransaction
from .serializers import PaymentTransactionSerializer


@api_view(['GET'])
@permission_classes((IsAdminOnly,))
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

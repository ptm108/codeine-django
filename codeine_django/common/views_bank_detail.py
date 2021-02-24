from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import (
    IsPartnerOnly,
    IsPartnerOrReadOnly
)
from .models import BankDetail, Partner
from .serializers import BankDetailSerializer

@api_view(['GET', 'POST'])
@permission_classes((IsPartnerOnly,))
def bank_detail_view(request):

    '''
    Get Bank Detail by Partner
    '''
    if request.method == 'GET':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)
            bank_detail = BankDetail.objects.get(partner=partner)

            serializer = BankDetailSerializer(bank_detail, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Create a new Bank Detail
    '''
    if request.method == 'POST':
        try: 
            data = request.data
            user = request.user
            partner = Partner.objects.get(user=user)

            bank_detail = BankDetail.objects.get(partner=partner)

            if bank_detail: # bank account details is already created
                return Response("Partner has an existing bank account", status=status.HTTP_409_CONFLICT)
            # end if

            bank_detail = BankDetail(
                bank_account=data['bank_account'],
                bank_name=data['bank_name'],
                swift_code=data['swift_code'],
                bank_country=data['bank_country'],
                bank_address=data['bank_address'],

                partner = partner
            )
            bank_detail.save()

            serializer = BankDetailSerializer(bank_detail, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes((IsPartnerOrReadOnly,))
def single_bank_detail_view(request, pk):

    '''
    Get Bank Detail by ID
    '''
    if request.method == 'GET':
        try:
            bank_detail = BankDetail.objects.get(pk=pk)

            serializer = BankDetailSerializer(bank_detail, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Update Bank Detail
    '''
    if request.method == 'PATCH':
        try: 
            data = request.data
            user = request.user
            bank_detail = BankDetail.objects.get(pk=pk)
            partner = bank_detail.partner

            # assert that request partner is the owner of the bank detail
            if partner.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            if 'bank_account' in data:
                bank_detail.bank_account = data['bank_account']
            if 'bank_name' in data:
                bank_detail.bank_name = data['bank_name']
            if 'swift_code' in data:
                bank_detail.swift_code = data['swift_code']
            if 'bank_country' in data:
                bank_detail.bank_country = data['bank_country']
            if 'bank_address' in data:
                bank_detail.bank_address = data['bank_address']
            # end ifs

            bank_detail.save()

            serializer = BankDetailSerializer(bank_detail, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Delete Bank Detail
    '''
    if request.method == 'DELETE':
        try: 
            user = request.user
            bank_detail = BankDetail.objects.get(pk=pk)
            partner = bank_detail.partner

            # assert that request partner is the owner of the bank detail
            if partner.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            bank_detail.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

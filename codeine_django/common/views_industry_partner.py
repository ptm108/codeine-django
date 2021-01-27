from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import BaseUser, IndustryPartner
from .serializers import IndustryPartnerSerializer


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def industry_partner_view(request):
    '''
    Get all industry providers
    Search by industry partner first names, last names or company name
    '''
    if request.method == 'GET':
        industry_partners = IndustryPartner.objects

        # extract params
        search = request.query_params.get('search', None)

        if search is not None:
            industry_partners = industry_partners.filter(
                Q(company_name__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
        # end if
        serializer = IndustryPartnerSerializer(industry_partners, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates/Register Industry Partner
    '''
    if request.method == 'POST':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.create_user(data['email'], data['password'], first_name=data['first_name'], last_name=data['last_name'])
                user.save()

                industry_partner = IndustryPartner(user=user, company_name=data['company_name'])
                member.save()

                serializer = IndustryPartnerSerializer(industry_partner, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if
    
# end def

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
    IsAdminUser,
)
from .models import BaseUser, IndustryPartner, CodeineAdmin
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
    Creates/Register industry partner
    '''
    if request.method == 'POST':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.create_user(data['email'], data['password'], first_name=data['first_name'], last_name=data['last_name'])
                user.save()

                industry_partner = IndustryPartner(user=user, company_name=data['company_name'])
                industry_partner.save()

                serializer = IndustryPartnerSerializer(industry_partner, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if
# end def

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@parser_classes((MultiPartParser, FormParser))
def single_industry_partner_view(request, pk):
    '''
    Gets a industry partner by primary key/id
    '''
    if request.method == 'GET':
        try:
            user = BaseUser.objects.get(pk=pk)
            industry_partner = IndustryPartner.objects.get(user=user)

            serializer = IndustryPartnerSerializer(industry_partner, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

    '''
    Updates a industry partner
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            with transaction.atomic():
                user = request.user
                industry_partner = IndustryPartner.objects.get(user=user)

                if 'first_name' in data:
                    user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                if 'email' in data:
                    user.email = data['email']
                if 'profile_photo' in data:
                    user.profile_photo = data['profile_photo']
                user.save()

                if 'company_name' in data:
                    industry_partner.company_name = data['company_name']
                if 'contact_number' in data:
                    industry_partner.contact_number = data['contact_number']
                industry_partner.save()
            # end with

            serializer = IndustryPartnerSerializer(industry_partner, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IndustryPartner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deactivates industry partner
    ''' 
    if request.method == 'DELETE':
        try:
            user = request.user
            base_user = BaseUser.objects.get(pk=pk)
            industry_partner = IndustryPartner.objects.get(user=user)

            # assert requesting industry partner is deleting own account
            if industry_partner.user != user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            industry_partner.user.is_active = False
            industry_partner.user.save()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Updates industry partner's password
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            user = request.user
            base_user = BaseUser.objects.get(pk=pk)
            industry_partner = IndustryPartner.objects.get(user=user)

            # assert requesting industry partner is editing own account
            if industry_partner.user != user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            # check old password
            if not user.check_password(data['old_password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            user.set_password(data['new_password'])
            user.save()

            industry_partner = user.industrypartner
            serializer = IndustryPartnerSerializer(industry_partner, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response('Invalid payload', status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['DELETE', 'POST'])
@permission_classes((IsAdminUser,))
def industry_partner_admin_view(request, pk):
    
    '''
    Admin deactivates industry partner
    ''' 
    if request.method == 'DELETE':
        try:
            industry_partner = IndustryPartner.objects.get(pk=pk)

            industry_partner.user.is_active = False
            industry_partner.user.save()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Admin activates industry partner
    ''' 
    if request.method == 'POST':
        try:
            industry_partner = IndustryPartner.objects.get(pk=pk)

            industry_partner.user.is_active = True
            industry_partner.user.save()
            
            serializer = IndustryPartnerSerializer(industry_partner, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

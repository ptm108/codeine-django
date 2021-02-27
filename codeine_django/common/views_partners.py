from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import BaseUser, Partner, Organization
from .serializers import NestedBaseUserSerializer
from .permissions import IsPartnerOnly, IsPartnerOrAdminOrReadOnly
import json
from django.template.loader import render_to_string
from django.core.mail import send_mail


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def partner_view(request):
    '''
    Creates a new Partner
    '''
    if request.method == 'POST':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.create_user(data['email'], data['password'], first_name=data['first_name'], last_name=data['last_name'])
                user.save()

                organization = None
                org_admin = False
                if 'organization_name' in data:
                    try:
                        organization = Organization.objects.get(organization_name=data['organization_name'])
                    except Organization.DoesNotExist:
                        organization = Organization(organization_name=data['organization_name'])
                        organization.save()
                        org_admin = True
                    # end try-except
                # end if

                partner = Partner(user=user, organization=organization, org_admin=org_admin)
                partner.save()

                name = user.first_name + ' ' + user.last_name

                verification_url = (
                    f'http://localhost:3000/verify/{user.id}'
                )
                recipient_email = (
                    data['email']
                )  

                plain_text_email = render_to_string(
                    'verification.txt', {'name': name, 'url': verification_url}
                )

                html_email = render_to_string(
                    'verification.html', {'name': name, 'url': verification_url}
                )

                send_mail(
                    'Welcome to Codeine!',
                    plain_text_email,
                    'Codeine Admin <codeine4103@gmail.com>',
                    [recipient_email], 
                    html_message=html_email,
                )

                serializer = NestedBaseUserSerializer(user, context={"request": request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get all Partners
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)
        is_active = request.query_params.get('is_active', None)

        users = BaseUser.objects.exclude(partner__isnull=True)

        if is_active is not None:
            active = json.loads(is_active.lower())
            users = users.filter(is_active=active)
        if search is not None:
            users = users.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        # end ifs

        serializer = NestedBaseUserSerializer(users.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsPartnerOrAdminOrReadOnly,))
@parser_classes((MultiPartParser, FormParser))
def single_partner_view(request, pk):
    '''
    Gets a partner by primary key/ id
    '''
    if request.method == 'GET':
        try:
            user = BaseUser.objects.get(pk=pk)

            return Response(NestedBaseUserSerializer(user, context={"request": request}).data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Updates a partner
    '''
    if request.method == 'PUT':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.get(pk=pk)
                partner = Partner.objects.get(user=user)

                if request.user != user and not partner.org_admin and not request.user.is_admin:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                # end if

                if 'first_name' in data:
                    user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                if 'email' in data:
                    user.email = data['email']
                if 'profile_photo' in data:
                    user.profile_photo = data['profile_photo']
                # end ifs
                user.save()

                partner = Partner.objects.get(user=user)

                if 'job_title' in data:
                    partner.job_title = data['job_title']
                if 'bio' in data:
                    partner.bio = data['bio']
                # if 'consultation_rate' in data:
                #     partner.consultation_rate = data['consultation_rate']
                if 'org_admin' in data:
                    partner.org_admin = data['org_admin']
                # end ifs
                partner.save()

                return Response(NestedBaseUserSerializer(user, context={"request": request}).data, status=status.HTTP_200_OK)
            except Member.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except (KeyError, ValueError, IntegrityError) as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Inactivates a partner
    '''
    if request.method == 'DELETE':
        try:
            user = BaseUser.objects.get(pk=pk)
            partner = Partner.objects.get(user=user)

            if request.user != user and not partner.org_admin and not request.user.is_admin:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            user.is_active = False  # mark as deleted
            user.save()

            return Response(status=status.HTTP_200_OK)

        except Member.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def partner_change_password_view(request, pk):
    '''
    Updates partner's password
    Only owner can update
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            user = request.user

            # check old password
            if not user.check_password(data['old_password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            user.set_password(data['new_password'])
            user.save()

            serializer = NestedBaseUserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response('Invalid payload', status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['POST'])
@permission_classes((AllowAny,))
def activate_partner_view(request, pk):
    '''
    Activates partner
    '''
    if request.method == 'POST':
        try:
            user = BaseUser.objects.get(pk=pk)
            partner = Partner.objects.get(user=user)

            user.is_active = True
            user.save()

            serializer = NestedBaseUserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

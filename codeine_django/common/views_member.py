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
from .models import BaseUser, Member
from .serializers import MemberSerializer, NestedBaseUserSerializer
from .permissions import IsMemberOnly, IsMemberOrAdminOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def member_view(request):
    '''
    Creates a new member
    '''
    if request.method == 'POST':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.create_user(data['email'], data['password'], first_name=data['first_name'], last_name=data['last_name'])
                user.save()

                member = Member(user=user)
                member.save()

                serializer = NestedBaseUserSerializer(user, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if

    '''
    Get all active members
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        users = BaseUser.objects.exclude(member__isnull=True).exclude(is_active=False)

        if search is not None:
            users = users.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        # end if

        serializer = NestedBaseUserSerializer(users.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsMemberOrAdminOrReadOnly,))
@parser_classes((MultiPartParser, FormParser))
def single_member_view(request, pk):
    '''
    Gets a member by primary key/ id
    '''
    if request.method == 'GET':
        try:
            user = BaseUser.objects.get(pk=pk)

            return Response(NestedBaseUserSerializer(user, context={"request": request}).data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

    '''
    Updates a member
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            user = BaseUser.objects.get(pk=pk)

            if request.user != user:
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
            user.save()

            return Response(NestedBaseUserSerializer(user, context={"request": request}).data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a member
    '''
    if request.method == 'DELETE':
        try:
            user = BaseUser.objects.get(pk=pk)
            member = Member.objects.get(user=user)

            if request.user != user:
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
@permission_classes((IsMemberOnly,))
def member_change_password_view(request, pk):
    '''
    Updates member's password
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
def activate_member_view(request, pk):
    '''
    Activates member
    '''
    if request.method == 'POST':
        try:
            user = BaseUser.objects.get(pk=pk)
            member = Member.objects.get(user=user)

            user.is_active = True
            user.save()

            serializer = NestedBaseUserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

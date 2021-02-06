from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from .models import BaseUser, CodeineAdmin, ContentProvider
from .serializers import CodeineAdminSerializer


@api_view(['POST', 'GET'])
@permission_classes((IsAdminUser,))
def admin_view(request):
    '''
    Creates a new admin
    '''
    if request.method == 'POST':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.create_user(data['email'], data['password'], is_admin=True, is_active=True, first_name=data['first_name'], last_name=data['last_name'])
                user.save()

                admin = CodeineAdmin(user=user)
                admin.save()

                serializer = CodeineAdminSerializer(admin, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if

    '''
    Retrieves all admin users
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        admins = CodeineAdmin.objects

        if search is not None:
            admins = admins.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        # end if

        serializer = CodeineAdminSerializer(admins.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAdminUser,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def single_admin_view(request, pk):
    '''
    Gets an admin by primary key/ id
    '''
    if request.method == 'GET':

        try:
            user = BaseUser.objects.get(pk=pk)
            admin = CodeineAdmin.objects.get(user=user)
           
            return Response(CodeineAdminSerializer(admin, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Updates an admin
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            user = request.user
            base_user = BaseUser.objects.get(pk=pk)
            admin = CodeineAdmin.objects.get(user=user)

            # assert requesting user is editing own account
            if user != base_user:
                return Response('User is not changing their own password', status=status.HTTP_400_BAD_REQUEST)
            # end if

            with transaction.atomic():
                if 'first_name' in data:
                    user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                if 'email' in data:
                    user.email = data['email']
                if 'profile_photo' in data:
                    user.profile_photo = data['profile_photo']
                user.save()
            # end with

            serializer = CodeineAdminSerializer(admin, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CodeineAdmin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes an admin
    '''
    if request.method == 'DELETE':
        try:
            user = BaseUser.objects.get(pk=pk)
            admin = CodeineAdmin.objects.get(user=user)
            
            user.is_active = False  # mark as deleted
            user.is_admin = False # remove admin privileges
            user.save()

            return Response(status=status.HTTP_200_OK)
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def admin_change_password_view(request, pk):
    '''
    Updates admin's password
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            user = request.user
            base_user = BaseUser.objects.get(pk=pk)
            admin = CodeineAdmin.objects.get(user=user)

            # assert requesting user is editing own account
            if user != base_user:
                return Response('User is not changing their own password', status=status.HTTP_400_BAD_REQUEST)
            # end if

            # check old password
            if not user.check_password(data['old_password']):
                return Response('Current password does not match', status=status.HTTP_400_BAD_REQUEST)
            # end if

            user.set_password(data['new_password'])
            user.save()

            admin = user.codeineadmin
            serializer = CodeineAdminSerializer(admin, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response('Invalid payload', status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def
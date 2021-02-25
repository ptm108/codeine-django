from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
)
from .models import BaseUser
from .serializers import NestedBaseUserSerializer
import json


@api_view(['GET',])
@permission_classes((IsAdminUser,))
def admin_view(request):
    '''
    Get all Admin Users 
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)
        is_active = request.query_params.get('is_active', None)

        users = BaseUser.objects.exclude(is_admin=False)

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

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes((IsAdminUser,))
def single_admin_view(request, pk):
    '''
    Get single Admin User by ID 
    '''
    if request.method == 'GET':
        try:
            user = BaseUser.objects.get(pk=pk)

            serializer = NestedBaseUserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except 
    # end if

    '''
    Updates a Admin User
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
            # end ifs
            user.save()

            serializer = NestedBaseUserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Updates a Admin User's password
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            user = BaseUser.objects.get(pk=pk)

            if request.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if 

            # check old password
            if not request.user.check_password(data['old_password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            user.set_password(data['new_password'])
            user.save()

            serializer = NestedBaseUserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes Admin User
    '''
    if request.method == 'DELETE':
        try:
            user = BaseUser.objects.get(pk=pk)

            if request.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if 
            
            user.is_active = False  # mark as deleted
            user.save()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def
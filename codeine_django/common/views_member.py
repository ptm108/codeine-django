from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import BaseUser, Member
from .serializers import MemberSerializer


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def create_member(request):
    '''
    Creates a new member
    '''
    if request.method == 'POST':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.create_user(data['email'], data['password'])
                user.save()

                member = Member(user=user, first_name=data['first_name'], last_name=data['last_name'])
                member.save()

                serializer = MemberSerializer(member)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if

    '''
    Get all members
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        members = Member.objects

        if search is not None:
            members = members.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        # end if

        serializer = MemberSerializer(members.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def single_member_view(request, pk):
    '''
    Gets a member by primary key/ id
    '''
    if request.method == 'GET':
        try:
            member = Member.objects.get(pk=pk)

            return Response(MemberSerializer(member).data)
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
            with transaction.atomic():
                member = Member.objects.get(pk=pk)
                member.first_name = data['first_name']
                member.last_name = data['last_name']
                member.save()

                user = member.user
                user.email = data['email']
                user.save()
            # end with

            serializer = MemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a member
    '''
    if request.method == 'DELETE':
        try:
            member = Member.objects.get(pk=pk)
            user = member.user
            user.is_active = False # mark as deleted
            user.save()

            return Response(status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
# end def

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def member_change_password_view(request, pk):
    '''
    Updates member's password
    '''
    if request.method == 'PATCH':
        try:
            user = request.user
            member = Member.objects.get(pk=pk)
            
            # assert requesting user is editing own account
            if member.user != user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            # check old password
            if not user.check_password(data['old_password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            user.set_password(data['new_password'])
            user.save()

            member = user.member
            serializer = MemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError: 
            return Response('Invalid payload', status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

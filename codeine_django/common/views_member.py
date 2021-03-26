from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)

import json
import jwt
import os
from django.template.loader import render_to_string
from django.core.mail import send_mail
from codeine_django import settings

from .models import BaseUser, Member
from .serializers import MemberSerializer, NestedBaseUserSerializer
from .permissions import IsMemberOnly, IsMemberOrAdminOrReadOnly
from courses.models import Enrollment
from courses.serializers import NestedEnrollmentSerializer


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
        # end with
    # end if

    '''
    Get all members
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)
        is_active = request.query_params.get('is_active', None)

        users = BaseUser.objects.exclude(member__isnull=True)

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
        # end try-except
    # end if

    '''
    Updates a member
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            user = BaseUser.objects.get(pk=pk)

            if request.user != user and not request.user.is_admin:
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
            if 'age' in data:
                user.age = data['age']
            if 'gender' in data:
                user.gender = data['gender']
            if 'location' in data:
                user.location = data['location']
            # end ifs
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

            if request.user != user and not request.user.is_admin:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            user.is_active = False  # mark as deleted
            user.save()

            return Response(status=status.HTTP_200_OK)

        except Member.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
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


@api_view(['POST', 'PATCH'])
@permission_classes((AllowAny,))
def reset_member_password_view(request):
    '''
    Sends email with jwt token to reset password
    '''
    if request.method == 'POST':

        try:
            data = request.data
            print(data)
            email = data['email']
            user = BaseUser.objects.get(email=email)
            name = user.first_name + ' ' + user.last_name

            refresh = RefreshToken.for_user(user)

            reset_password_url = (
                f'http://localhost:3000/reset-password/?token={refresh.access_token}'
            )
            recipient_email = (
                data['email']
            )

            plain_text_email = render_to_string(
                'reset_password.txt', {'name': name, 'url': reset_password_url}
            )

            html_email = render_to_string(
                'reset_password.html', {'name': name, 'url': reset_password_url}
            )

            send_mail(
                'Ask and you shall receive... a password reset',
                plain_text_email,
                'Codeine Admin <codeine4103@gmail.com>',
                [recipient_email],
                html_message=html_email,
            )

            return Response(status=status.HTTP_200_OK)

        except (IntegrityError, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Reset member's password
    '''
    if request.method == 'PATCH':
        try:
            data = request.data
            user = request.user

            # # extract query params
            # token = request.query_params.get('token', None)
            # payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
            # user = BaseUser.objects.get(id=payload['user_id'])

            user.set_password(data['reset_password'])
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


@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def suspend_user_view(request, pk):
    '''
    Suspend/Unsuspend user
    '''
    if request.method == 'PATCH':
        try:
            user = BaseUser.objects.get(pk=pk)
            member = Member.objects.get(user=user)
            data = request.data

            user.is_suspended = data['is_suspended']
            user.save()

            serializer = NestedBaseUserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((AllowAny,))
def public_member_course_view(request, pk):
    '''
    Public view to get member's courses
    '''
    if request.method == 'GET':
        try:
            user = BaseUser.objects.get(pk=pk)
            enrollments = Enrollment.objects.filter(member__user=user)

            serializer = NestedEnrollmentSerializer(enrollments.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

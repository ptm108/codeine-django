from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import BaseUser, ContentProvider
from .serializers import ContentProviderSerializer


@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
def content_provider_view(request):
    '''
    Creates a new content provider
    '''
    if request.method == 'POST':
        data = request.data

        with transaction.atomic():
            try:
                user = BaseUser.objects.create_user(data['email'], data['password'], first_name=data['first_name'], last_name=data['last_name'])
                user.save()

                content_provider = ContentProvider(user=user, company_name=data['company_name'], job_title=data['job_title'], bio=data['bio'])
                content_provider.save()

                serializer = ContentProviderSerializer(content_provider)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if

    '''
    Retrieves all content providers
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        content_providers = ContentProvider.objects

        if search is not None:
            content_providers = content_providers.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        # end if

        serializer = ContentProviderSerializer(content_providers.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@parser_classes((MultiPartParser, FormParser))
def single_content_provider_view(request, pk):
    '''
    Gets a content provider by primary key/ id
    '''
    if request.method == 'GET':

        try:
            content_provider = ContentProvider.objects.get(pk=pk)
           
            return Response(ContentProviderSerializer(content_provider, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Updates a content provider
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            with transaction.atomic():
                content_provider = ContentProvider.objects.get(pk=pk)
                user = content_provider.user

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
                    content_provider.company_name = data['company_name']
                if 'job_title' in data:
                    content_provider.job_title = data['job_title']
                if 'bio' in data:
                    content_provider.bio = data['bio']
                content_provider.save()
            # end with

            serializer = ContentProviderSerializer(content_provider, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a content provider
    '''
    if request.method == 'DELETE':
        try:
            content_provider = ContentProvider.objects.get(pk=pk)
            user = content_provider.user
            user.is_active = False  # mark as deleted
            user.save()

            return Response(status=status.HTTP_200_OK)
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def content_provider_change_password_view(request, pk):
    '''
    Updates content providers's password
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(pk=pk)

            # assert requesting user is editing own account
            if content_provider.user != user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            # check old password
            if not user.check_password(data['old_password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            user.set_password(data['new_password'])
            user.save()

            content_provider = user.contentprovider
            serializer = ContentProviderSerializer(content_provider, context={"request": request})
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
def activate_content_provider_view(request, pk):
    '''
    Activates content provider
    ''' 
    if request.method == 'POST':
        try:
            content_provider = ContentProvider.objects.get(pk=pk)
            user = content_provider.user

            user.is_active = True
            user.save()
            
            serializer = ContentProviderSerializer(content_provider, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def content_provider_update_consultation_rate(request, pk):
    '''
    Updates content providers's consultation rate
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(pk=pk)

            # assert requesting user is editing own account
            if content_provider.user != user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            content_provider.consultation_rate = data['consultation_rate']
            serializer = ContentProviderSerializer(content_provider, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response('Invalid payload', status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

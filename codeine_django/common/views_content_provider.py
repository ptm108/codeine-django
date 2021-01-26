from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
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
                user = BaseUser.objects.create_user(data['email'], data['password'])
                user.save()

                content_provider = ContentProvider(user=user, first_name=data['first_name'], last_name=data['last_name'], company_name=data['company_name'], job_title=data['job_title'], bio=data['bio'])
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
        try:
            content_providers = ContentProvider.objects.all()
            return Response(content_providers, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    return Response({'message': 'Unsupported'}, status=status.HTTP_400_BAD_REQUEST)

# end def

@api_view(['GET', 'PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def protected_content_provider_view(request, pk):
    '''
    Get current user
    '''
    if request.method == 'GET':

        try:
            content_provider = ContentProvider.objects.get(pk=pk)
            return Response(content_provider, status=status.HTTP_200_OK)
           
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Activate or deactivates current user
    '''
    if request.method == 'PATCH':
        data = request.data

        try:
            content_provider = ContentProvider.objects.get(pk=pk)
            is_active = self.request.query_params.get('active')
            content_provider.is_active = is_active
            content_provider.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
           
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

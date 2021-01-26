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


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_content_provider(request):
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

                serializer = MemberSerializer(content_provider)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # end with
    # end if
# end def

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_content_providers(request):
    '''
    Retrieves all content providers
    '''
    if request.method == 'GET':
        try:
            content_providers = ContentProvider.objects.all()
            serializer = ContentProviderSerializer(content_providers, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    return Response({'message': 'Unsupported'}, status=status.HTTP_400_BAD_REQUEST)
# end def

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def protected_content_provider_view(request, pk):
    '''
    Get current user
    '''
    if request.method == 'GET':

        try:
            content_provider = ContentProvider.objects.get(pk=pk)
            serializer = ContentProviderSerializer(content_provider, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
           
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PUT'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def activate_content_provider(request, pk):
    '''
    Activates current user
    '''
    if request.method == 'PUT':
        data = request.data

        try:
            content_provider = ContentProvider.objects.get(pk=pk)
            content_provider.is_active = True
            content_provider.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
           
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

@api_view(['PUT'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def deactivate_content_provider(request, pk):
    '''
    Deactivates current user
    '''
    if request.method == 'PUT':
        data = request.data

        try:
            content_provider = ContentProvider.objects.get(pk=pk)
            content_provider.is_active = False
            content_provider.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
           
        except ContentProvider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

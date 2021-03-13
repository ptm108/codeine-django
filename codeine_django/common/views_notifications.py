from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import json

from .permissions import AdminOrReadOnly
from .models import Notification, BaseUser
from .serializers import NotificationSerializer


@api_view(['GET', 'POST'])
@permission_classes((AdminOrReadOnly,))
def notification_view(request):
    '''
    Get all Notifications 
    '''
    if request.method == 'GET':
        user = request.user
        notifications = Notification.objects

        # extract query params
        search = request.query_params.get('search', None)
        is_read = request.query_params.get('is_read', None)
        is_receiver = request.query_params.get('is_receiver', None)

        if search is not None:
            notifications = notifications.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        if is_read is not None:
            notifications = notifications.filter(is_read=is_read)
        if is_receiver is not None:
            if is_receiver:
                notifications = notifications.filter(receiver=user)
            # end if
        # end ifs

        serializer = NotificationSerializer(
            notifications.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
    
    '''
    Create a new Notification
    '''
    if request.method == 'POST':
        try: 
            data = request.data
            receiver = BaseUser.objects.get(pk=data['receiver_id'])

            notification = Notification(
                title=data['title'],
                description=data['description'],
                receiver=receiver
            )
            notification.save()

            serializer = NotificationSerializer(notification, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((AdminOrReadOnly,))
def single_notification_view(request, pk):
    '''
    Get single Notification by ID 
    '''
    if request.method == 'GET':
        try:
            notification = Notification.objects.get(pk=pk)

            serializer = NotificationSerializer(
                notification, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Updates a Notification
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            notification = Notification.objects.get(pk=pk)

            if 'title' in data:
                notification.title = data['title']
            if 'description' in data:
                notification.description = data['description']
            if 'is_read' in data:
                notification.is_read = data['is_read']
            # end ifs
            notification.save()

            serializer = NotificationSerializer(
                notification, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes Notification
    '''
    if request.method == 'DELETE':
        try:
            notification = Notification.objects.get(pk=pk)
            notification.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

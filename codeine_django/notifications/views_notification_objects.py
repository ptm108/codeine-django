from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import json

from rest_framework.permissions import IsAuthenticated
from .models import NotificationObject
from common.models import BaseUser
from .serializers import NotificationObjectSerializer


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def notification_object_view(request):
    '''
    Get User's Notifications
    '''
    if request.method == 'GET':
        user = request.user
        notification_objects = NotificationObject.objects.filter(receiver=user)

        # extract query params
        search = request.query_params.get('search', None)
        is_read = request.query_params.get('is_read', None)

        if search is not None:
            notification_objects = notification_objects.filter(
                Q(notification__title__icontains=search) |
                Q(notification__description__icontains=search)
            )
        if is_read is not None:
            notification_objects = notification_objects.filter(is_read=is_read)
        # end ifs

        serializer = NotificationObjectSerializer(
            notification_objects.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated,))
def single_notification_object_view(request, pk):
    '''
    Get single Notification Object by ID 
    '''
    if request.method == 'GET':
        try:
            notification_object = NotificationObject.objects.get(pk=pk)
            serializer = NotificationObjectSerializer(
                notification_object, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes Notification Object
    '''
    if request.method == 'DELETE':
        try:
            user = request.user
            notification_object = NotificationObject.objects.get(pk=pk)

            if notification_object.receiver != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            notification_object.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def mark_notification_as_read(request, pk):
    '''
    Mark notification object as read
    '''
    if request.method == 'PATCH':
        try:
            notification_object = NotificationObject.objects.get(pk=pk)

            user = request.user
            if notification_object.receiver != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            notification_object.is_read = True
            notification_object.save()

            serializer = NotificationObjectSerializer(
                notification_object, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def mark_notification_as_unread(request, pk):
    '''
    Mark notification object as unread
    '''
    if request.method == 'PATCH':
        try:
            notification_object = NotificationObject.objects.get(pk=pk)

            user = request.user
            if notification_object.receiver != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            notification_object.is_read = False
            notification_object.save()

            serializer = NotificationObjectSerializer(
                notification_object, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def mark_multiple_as_read(request):
    '''
    Mark multiple notification object as read
    '''
    if request.method == 'PATCH':
        try:
            data = request.data
            user = request.user
            notification_objects = NotificationObject.objects.filter(receiver=user)

            if 'notification_object_ids' in data:
                notification_object_ids = data['notification_object_ids']
                for index, notification_object_id in enumerate(notification_object_ids):
                    notification_object = NotificationObject.objects.get(pk=notification_object_id)
                    if notification_object not in notification_objects:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        notification_object.is_read = True
                        notification_object.save()
                    # end if-else
                # end for
            # end if

            serializer = NotificationObjectSerializer(
                notification_objects.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def mark_multiple_as_unread(request):
    '''
    Mark multiple notification object as unread
    '''
    if request.method == 'PATCH':
        try:
            data = request.data
            user = request.user
            notification_objects = NotificationObject.objects.filter(receiver=user)

            if 'notification_object_ids' in data:
                notification_object_ids = data['notification_object_ids']
                for index, notification_object_id in enumerate(notification_object_ids):
                    notification_object = NotificationObject.objects.get(pk=notification_object_id)
                    if notification_object not in notification_objects:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        notification_object.is_read = False
                        notification_object.save()
                    # end if-else
                # end for
            # end if

            serializer = NotificationObjectSerializer(
                notification_objects.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def mark_multiple_as_read(request):
    '''
    Mark multiple notification object as read
    '''
    if request.method == 'PATCH':
        try:
            data = request.data
            user = request.user
            notification_objects = NotificationObject.objects.filter(receiver=user)

            if 'notification_object_ids' in data:
                notification_object_ids = data['notification_object_ids']
                for index, notification_object_id in enumerate(notification_object_ids):
                    notification_object = NotificationObject.objects.get(pk=notification_object_id)
                    if notification_object not in notification_objects:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        notification_object.is_read = True
                        notification_object.save()
                    # end if-else
                # end for
            # end if

            serializer = NotificationObjectSerializer(
                notification_objects.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def mark_all_as_read(request):
    '''
    Mark all notification objects as read
    '''
    if request.method == 'PATCH':
        try:
            data = request.data
            user = request.user
            notification_objects = NotificationObject.objects.filter(receiver=user)

            for notification_object in notification_objects:
                notification_object.is_read = True
                notification_object.save()
            # end for

            serializer = NotificationObjectSerializer(
                notification_objects.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def mark_all_as_unread(request):
    '''
    Mark all notification objects as unread
    '''
    if request.method == 'PATCH':
        try:
            data = request.data
            user = request.user
            notification_objects = NotificationObject.objects.filter(receiver=user)

            for notification_object in notification_objects:
                notification_object.is_read = False
                notification_object.save()
            # end for

            serializer = NotificationObjectSerializer(
                notification_objects.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

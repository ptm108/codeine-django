from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import json

from common.permissions import IsPartnerOrAdminOrReadOnly

from .models import Notification, NotificationObject
from .serializers import NotificationSerializer
from common.models import BaseUser, PaymentTransaction
from courses.models import Course
from community.models import Article, CodeReview
from industry_projects.models import IndustryProject
from consultations.models import ConsultationSlot
from helpdesk.models import Ticket

import json


@api_view(['GET', 'POST'])
@permission_classes((IsPartnerOrAdminOrReadOnly,))
def notification_view(request):
    '''
    Get all Notifications
    '''
    if request.method == 'GET':
        notifications = Notification.objects
        user = request.user

        # extract query params
        search = request.query_params.get('search', None)
        is_sender = request.query_params.get('is_sender', None)

        if search is not None:
            notifications = notifications.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if is_sender is not None:
            is_sender = json.loads(is_sender.lower())
            if is_sender:
                notifications = notifications.filter(sender=user)
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
            user = request.user

            notification = Notification(
                title=data['title'],
                description=data['description'],
                notification_type=data['notification_type'],
                sender=user
            )

            if 'photo' in data:
                notification.photo = data['photo']
            if 'course_id' in data:
                course_id = data['course_id']
                notification.course = Course.objects.get(pk=course_id)
            if 'article_id' in data:
                article_id = data['article_id']
                notification.article = Article.objects.get(pk=article_id)
            if 'code_review_id' in data:
                code_review_id = data['code_review_id']
                notification.code_review = CodeReview.objects.get(
                    pk=code_review_id)
            if 'transaction_id' in data:
                transaction_id = data['transaction_id']
                notification.transaction = PaymentTransaction.objects.get(
                    pk=transaction_id)
            if 'consultation_slot_id' in data:
                consultation_slot_id = data['consultation_slot_id']
                notification.consultation_slot = ConsultationSlot.objects.get(
                    pk=consultation_slot_id)
            if 'ticket_id' in data:
                ticket_id = data['ticket_id']
                notification.ticket = Ticket.objects.get(pk=ticket_id)
            if 'industry_project_id' in data:
                industry_project_id = data['industry_project_id']
                notification.industry_project = IndustryProject.objects.get(
                    pk=industry_project_id)
            # end ifs

            notification.save()

            # create notification objects
            if 'receiver_ids' in data:
                receiver_ids = json.loads(data['receiver_ids'])
                for index, receiver_id in enumerate(receiver_ids):
                    receiver = BaseUser.objects.get(pk=receiver_id)
                    notification_object = NotificationObject(receiver=receiver, notification=notification)
                    notification_object.save()
                # end for
            # end if

            serializer = NotificationSerializer(notification, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsPartnerOrAdminOrReadOnly,))
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
    Deletes Notification
    '''
    if request.method == 'DELETE':
        try:
            notification = Notification.objects.get(pk=pk)
            
            user = request.user
            if notification.sender != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            notification.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

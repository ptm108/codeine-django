from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from .models import Article, Engagement
from .serializers import EngagementSerializer
from common.models import Member

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def engagement_view(request, article_id):
    '''
    Retrieves all engagements
    '''
    if request.method == 'GET':
        article = Article.objects.get(pk=article_id)
        engagements = Engagement.objects.filter(article=article)

        # extract query params
        is_user = request.query_params.get('is_user', None)

        if is_user is not None:
            if is_user:
                user = request.user
                member = Member.objects.get(user=user)
                engagements = engagements.filter(
                    Q(member=member)
                )
        # end if

        serializer = EngagementSerializer(
            engagements.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new engagement
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data
        member = Member.objects.get(user=user)
        article = Article.objects.get(pk=article_id)

        if Engagement.objects.filter(Q(member=member) & Q(article=article)).exists():
            # engagement not unique
            return Response(status=status.HTTP_403_FORBIDDEN)
        # end if
        try:
            engagement = Engagement(
                like=data['like'],
                member=member,
                article=article
            )
            engagement.save()

            serializer = EngagementSerializer(
                engagement, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def single_engagement_view(request, pk, article_id):
    '''
    Get an engagement by primary key/ id
    '''
    if request.method == 'GET':
        try:
            engagement = Engagement.objects.get(pk=pk)
            serializer = EngagementSerializer(
                engagement, context={'request': request})
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Update engagement - like
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            engagement = Engagement.objects.get(pk=pk)

            if 'like' in data:
                engagement.like = data['like']

            engagement.save()
            serializer = EngagementSerializer(
                engagement, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Engagement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Deletes an engagement
    '''
    if request.method == 'DELETE':
        try:
            engagement = Engagement.objects.get(pk=pk)
            engagement.delete()
            return Response(status=status.HTTP_200_OK)
        except Engagement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # end if
# def

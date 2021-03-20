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
from .models import CodeReview, CodeReviewEngagement
from .serializers import CodeReviewEngagementSerializer

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def code_review_engagement_view(request, code_review_id):
    '''
    Retrieves all engagements
    '''
    if request.method == 'GET':
        code_review = CodeReview.objects.get(pk=code_review_id)
        code_review_engagements = CodeReviewEngagement.objects.filter(code_review=code_review)

        # extract query params
        is_user = request.query_params.get('is_user', None)

        if is_user is not None:
            if is_user:
                user = request.user
                code_review_engagements = code_review_engagements.filter(
                    Q(user=user)
                )
        # end if

        serializer = CodeReviewEngagementSerializer(
            code_review_engagements.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new engagement
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data
        code_review = CodeReview.objects.get(pk=code_review_id)

        if CodeReviewEngagement.objects.filter(Q(user=user) & Q(code_review=code_review)).exists():
            # CodeReviewEngagement not unique
            return Response(status=status.HTTP_403_FORBIDDEN)
        # end if
        try:
            code_review_engagement = CodeReviewEngagement(
                like=data['like'],
                user=user,
                code_review=code_review
            )
            code_review_engagement.save()

            serializer = CodeReviewEngagementSerializer(
                code_review_engagement, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def single_code_review_engagement_view(request, pk, code_review_id):
    '''
    Get an code reivew engagement by primary key/ id
    '''
    if request.method == 'GET':
        try:
            code_review_engagement = CodeReviewEngagement.objects.get(pk=pk)
            serializer = CodeReviewEngagementSerializer(
                code_review_engagement, context={'request': request})
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Update CodeReviewEngagement - like
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            code_review_engagement = CodeReviewEngagement.objects.get(pk=pk)

            if 'like' in data:
                code_review_engagement.like = data['like']

            code_review_engagement.save()
            serializer = CodeReviewEngagementSerializer(
                code_review_engagement, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CodeReviewEngagement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Deletes an CodeReview Engagement
    '''
    if request.method == 'DELETE':
        try:
            code_review_engagement = CodeReviewEngagement.objects.get(pk=pk)
            code_review_engagement.delete()
            return Response(status=status.HTTP_200_OK)
        except CodeReviewEngagement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # end if
# def

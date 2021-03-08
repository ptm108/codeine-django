from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from .models import CodeReview
from .serializers import CodeReviewSerializer
from common.models import Member

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def code_review_view(request):
    '''
    Retrieves all code reviews
    '''
    if request.method == 'GET':
        code_reviews = CodeReview.objects

        # extract query params
        search = request.query_params.get('search', None)

        if search is not None:
            articles = articles.filter(
                Q(member__user__id__icontains=search) |
                Q(title__icontains=search) |
                Q(code__icontains=search) |
                Q(coding_languages__icontains=search) |
                Q(categories__icontains=search)
            )
        # end if
        serializer = CodeReviewSerializer(code_reviews.all(), many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new code review
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data
        member = Member.objects.get(user=user)

        try:
            code_review = CodeReview(
                title=data['title'],
                code=data['code'],
                coding_languages=data['coding_languages'],
                categories=data['categories'],
                member=member
            )
            code_review.save()

            serializer = CodeReviewSerializer(code_review, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def single_code_review_view(request, pk):
    '''
    Get a code review by primary key/ id
    '''
    if request.method == 'GET':
        try:
            code_review = CodeReview.objects.get(pk=pk)
            serializer = CodeReviewSerializer(
                code_review, context={'request': request})
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Update title, code, coding_languages, categories
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            code_review = CodeReview.objects.get(pk=pk)

            if 'title' in data:
                code_review.title = data['title']
            if 'code' in data:
                code_review.code = data['code']
            if 'category' in data:
                code_review.category = data['category']
            if 'coding_languages' in data:
                code_review.coding_languages = data['coding_languages']
            if 'categories' in data:
                code_review.categories = data['categories']

            code_review.save()
            serializer = CodeReviewSerializer(
                code_review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CodeReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Deletes a code review
    '''
    if request.method == 'DELETE':
        try:
            code_review = CodeReview.objects.get(pk=pk)
            code_review.delete()
            return Response(status=status.HTTP_200_OK)
        except CodeReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# def

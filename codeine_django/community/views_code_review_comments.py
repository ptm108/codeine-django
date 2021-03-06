from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import CodeReview, CodeReviewComment
from .serializers import CodeReviewCommentSerializer
from common.models import Member

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def code_review_comment_view(request, code_review_id):
    '''
    Retrieves all code review comments
    '''
    if request.method == 'GET':
        code_review = CodeReview.objects.get(pk=code_review_id)
        code_review_comments = CodeReviewComment.objects.filter(code_review=code_review)
        
        # extract query params
        search = request.query_params.get('search', None)

        if search is not None:
            code_review_comments = code_review_comments.filter(
                Q(highlighted_code__icontains=search) |
                Q(comment__icontains=search) |
                Q(user__id__icontains=search) |
                Q(code_review__id__icontains=search)
            )
        # end if

        serializer = CodeReviewCommentSerializer(code_review_comments.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new code review comment
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data
        code_review = CodeReview.objects.get(pk=code_review_id)
        parent_comment = None
        if 'parent_comment_id' in data:
            parent_comment = CodeReviewComment.objects.get(pk=data['parent_comment_id'])

        try:
            code_review_comment = CodeReviewComment(
                highlighted_code = data['highlighted_code'],
                comment = data['comment'],
                user = user,
                code_review = code_review,
                parent_comment = parent_comment
            )
            code_review_comment.save()
            serializer = CodeReviewCommentSerializer(code_review_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def single_code_review_comment_view(request, code_review_id, pk):
    '''
    Get an code review comment by primary key/ id
    '''
    if request.method == 'GET':
        try:
            code_review_comment = CodeReviewComment.objects.get(pk=pk)
            serializer = CodeReviewCommentSerializer(code_review_comment)
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
    '''
    Update code review comment
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            code_review_comment = CodeReviewComment.objects.get(pk=pk)

            if 'highlighted_code' in data:
                code_review_comment.highlighted_code = data['highlighted_code']
            if 'comment' in data:
                code_review_comment.comment = data['comment']

            code_review_comment.save()
            serializer = CodeReviewCommentSerializer(code_review_comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CodeReviewComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Deletes code review comment
    '''
    if request.method == 'DELETE':
        try:
            code_review_comment = CodeReviewComment.objects.get(pk=pk)
            code_review_comment.delete()
            return Response(status=status.HTTP_200_OK)
        except CodeReviewComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# def

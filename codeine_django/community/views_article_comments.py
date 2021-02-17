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
from .models import Article, ArticleComment
from .serializers import ArticleCommentSerializer
from common.models import Member

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def article_comment_view(request, article_id):
    '''
    Retrieves all article comments
    '''
    if request.method == 'GET':
        article = Article.objects.get(pk=article_id)
        article_comments = ArticleComment.objects.filter(article=article)
        
        # extract query params
        search = request.query_params.get('search', None)

        if search is not None:
            article_comments = article_comments.filter(
                Q(comment__icontains=search)
            )
        # end if

        serializer = ArticleCommentSerializer(article_comments.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new article comment
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data
        article = Article.objects.get(pk=article_id)
        parent_comment = None
        if 'parent_comment_id' in data:
            parent_comment = ArticleComment.objects.get(pk=data['parent_comment_id'])

        try:
            article_comment = ArticleComment(
                comment = data['comment'],
                user = user,
                article = article,
                parent_comment = parent_comment
            )
            article_comment.save()

            serializer = ArticleCommentSerializer(article_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
# def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def single_article_comment_view(request, article_id, pk):
    '''
    Get an article comment by primary key/ id
    '''
    if request.method == 'GET':
        try:
            article_comment = ArticleComment.objects.get(pk=pk)
            serializer = ArticleCommentSerializer(article_comment)
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # end if
    '''
    Update comment
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            article_comment = ArticleComment.objects.get(pk=pk)

            if 'comment' in data:
                article_comment.comment = data['comment']

            article_comment.save()
            serializer = ArticleCommentSerializer(article_comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Deletes an article
    '''
    if request.method == 'DELETE':
        try:
            article_comment = ArticleComment.objects.get(pk=pk)
            article_comment.delete()
            return Response(status=status.HTTP_200_OK)
        except ArticleComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # end if
# def
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
from .models import Article, ArticleComment
from .serializers import NestedArticleCommentSerializer
from common.models import Member

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def article_comment_view(request, article_id):
    '''
    Retrieves all article comments
    '''
    if request.method == 'GET':
        article = Article.objects.get(pk=article_id)
        article_comments = ArticleComment.objects.filter(article=article)

        # return first two levels of comments under article
        article_comments = article_comments.filter(reply_to=None)
        
        # extract query params
        search = request.query_params.get('search', None)

        if search is not None:
            article_comments = article_comments.filter(
                Q(comment__icontains=search)
            )
        # end if

        serializer = NestedArticleCommentSerializer(
            article_comments.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new article comment
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data

        try:
            article = Article.objects.get(pk=article_id)
            comment_count = ArticleComment.objects.filter(article=article).count()
            reply_to = None
        
            if 'reply_to' in data:
                reply_to = ArticleComment.objects.get(
                    pk=data['reply_to'])

            article_comment = ArticleComment(
                comment=data['comment'],
                user=user,
                article=article,
                reply_to=reply_to,
                display_id=comment_count + 1
            )
            article_comment.save()

            serializer = NestedArticleCommentSerializer(
                article_comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def single_article_comment_view(request, article_id, pk):
    '''
    Get an article comment by primary key/ id
    '''
    if request.method == 'GET':
        try:
            article_comment = ArticleComment.objects.get(pk=pk)
            serializer = NestedArticleCommentSerializer(
                article_comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Update comment
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            article_comment = ArticleComment.objects.get(pk=pk)

            if article_comment.user != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            if 'comment' in data:
                article_comment.comment = data['comment']

            article_comment.save()
            serializer = NestedArticleCommentSerializer(
                article_comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArticleComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes an article comment
    '''
    if request.method == 'DELETE':
        try:
            article_comment = ArticleComment.objects.get(pk=pk)
            
            if article_comment.user != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            article_comment.delete()
            return Response(status=status.HTTP_200_OK)
        except ArticleComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# def

@api_view(['PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def pin_comment_view(request, comment_id):
    '''
    Pins comment
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            article_comment = ArticleComment.objects.get(pk=pk)

            if article_comment.user != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            article_comment.pinned = True
            article_comment.save()

            article_comment.save()
            serializer = ArticleCommentSerializer(
                article_comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArticleComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def unpin_comment_view(request, comment_id):
    '''
    Unpins comment
    '''
    if request.method == 'PATCH':
        data = request.data
        try:
            article_comment = ArticleComment.objects.get(pk=pk)

            if article_comment.user != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            article_comment.pinned = False
            article_comment.save()

            article_comment.save()
            serializer = ArticleCommentSerializer(
                article_comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArticleComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


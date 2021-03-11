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
from .models import Article
from .serializers import ArticleSerializer
from common.models import Member

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def article_view(request):
    '''
    Retrieves all articles
    '''
    if request.method == 'GET':
        articles = Article.objects

        # extract query params
        search = request.query_params.get('search', None)

        if search is not None:
            articles = articles.filter(
                Q(member__user__id__exact=search) |
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(category__icontains=search)
            )
        # end if

        serializer = ArticleSerializer(
            articles.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if

    '''
    Creates a new article
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data
        member = Member.objects.get(user=user)

        try:
            article = Article(
                title=data['title'],
                content=data['content'],
                coding_languages=data['coding_languages'],
                languages=data['languages'],
                categories=data['categories'],
                member=member
            )
            article.save()

            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError, ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def single_article_view(request, pk):
    '''
    Get an article by primary key/ id
    '''
    if request.method == 'GET':
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
    '''
    Update title, content, category, is_published, is_activated
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            article = Article.objects.get(pk=pk)

            if 'title' in data:
                article.title = data['title']
            if 'content' in data:
                article.content = data['content']
            if 'category' in data:
                article.category = data['category']
            if 'is_published' in data:
                article.is_published = data['is_published']
            if 'is_activated' in data:
                article.is_activated = data['is_activated']

            article.save()
            serializer = ArticleSerializer(
                article, context={'request': request})
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
            article = Article.objects.get(pk=pk)
            article.delete()
            return Response(status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# def

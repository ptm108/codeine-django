from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

import json

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from common.permissions import AdminOrReadOnly
from .models import Article, ArticleEngagement
from .serializers import ArticleSerializer

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def article_view(request):
    '''
    Retrieves all articles
    '''
    if request.method == 'GET':
        articles = Article.objects.filter(
            Q(is_published=True) & Q(is_activated=True))

        # extract query params
        search = request.query_params.get('search', None)
        date_sort = request.query_params.get('sortDate', None)
        # get pagination params from request, default is (10, 1)
        page_size = int(request.query_params.get('pageSize', 1000))


        if search is not None:
            articles = articles.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(coding_languages__icontains=search) |
                Q(categories__icontains=search)
            )
        # end if

        if date_sort is not None:
            articles = articles.order_by(date_sort)
        # end if

        # paginator configs
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        result_page = paginator.paginate_queryset(articles.all(), request)
        serializer = ArticleSerializer(
            result_page, many=True, context={'request': request, 'public': True})
        return paginator.get_paginated_response(serializer.data)
    # end if

    '''
    Creates a new article
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data

        try:
            article = Article(
                title=data['title'],
                content=data['content'],
                coding_languages=data['coding_languages'],
                languages=data['languages'],
                categories=data['categories'],
                user=user
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
            user = request.user

            if article.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            if 'title' in data:
                article.title = data['title']
            if 'content' in data:
                article.content = data['content']
            # if 'is_published' in data:
            #     article.is_published = data['is_published']
            # if 'is_activated' in data:
            #     article.is_activated = data['is_activated']
            if 'coding_languages' in data:
                article.coding_languages = data['coding_languages']
            if 'languages' in data:
                article.languages = data['languages']
            if 'categories' in data:
                article.categories = data['categories']

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

            user = request.user

            if article.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            article.delete()
            return Response(status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# def


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def user_article_view(request):
    '''
    Retrieves all of user's code reviews
    '''
    if request.method == 'GET':
        user = request.user
        articles = Article.objects.filter(user=user)
        serializer = ArticleSerializer(
            articles.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# def


@api_view(['PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def publish_article_view(request, pk):
    '''
    Publish article by primary key/ id
    '''
    if request.method == 'PATCH':
        try:
            article = Article.objects.get(pk=pk)

            user = request.user

            if article.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            article.is_published = True
            article.save()
            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def unpublish_article_view(request, pk):
    '''
    Unpublish article by primary key/ id
    '''
    if request.method == 'PATCH':
        try:
            article = Article.objects.get(pk=pk)

            user = request.user

            if article.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            article.is_published = False
            article.save()
            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def article_engagement_view(request, pk):
    '''
    Like an Article
    '''
    if request.method == 'POST':
        user = request.user
        try:
            article = Article.objects.get(pk=pk)

            if ArticleEngagement.objects.filter(article=article).filter(user=user).exists():
                return Response(ArticleSerializer(article, context={'request': request, 'recursive': True}).data, status=status.HTTP_409_CONFLICT)
            # end if

            article_engagement = ArticleEngagement(
                user=user,
                article=article
            )
            article_engagement.save()

            serializer = ArticleSerializer(
                article, context={'request': request, 'recursive': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Unlike an Article
    '''
    if request.method == 'DELETE':
        user = request.user
        try:
            article = Article.objects.get(pk=pk)

            engagement = ArticleEngagement.objects.filter(
                article=article).get(user=user)
            engagement.delete()
            article.save()

            serializer = ArticleSerializer(
                article, context={'request': request, 'recursive': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((AdminOrReadOnly,))
def activate_article_view(request, pk):
    '''
    Activate article by primary key/ id
    '''
    if request.method == 'PATCH':
        try:
            article = Article.objects.get(pk=pk)

            user = request.user

            article.is_activated = True
            article.save()
            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def


@api_view(['PATCH'])
@permission_classes((AdminOrReadOnly,))
def deactivate_article_view(request, pk):
    '''
    Deactivate article by primary key/ id
    '''
    if request.method == 'PATCH':
        try:
            article = Article.objects.get(pk=pk)

            user = request.user

            article.is_activated = False
            article.save()
            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# def

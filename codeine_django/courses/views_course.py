from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import Course, Chapter, CourseMaterial
from .serializers import CourseSerializer
from common.models import ContentProvider

import json


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def course_view(request):
    '''
    Get/ Search all courses
    Params: search, sort
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)
        date_sort = request.query_params.get('sortDate', None)
        price_sort = request.query_params.get('sortPrice', None)
        rating_sort = request.query_params.get('sortRating', None)

        # get pagination params from request, default is (10, 1)
        page_size = int(request.query_params.get('pagesize', 10))

        courses = Course.objects

        if search is not None:
            courses = courses.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(coding_languages__icontains=search) |
                Q(categories__icontains=search) |
                Q(content_provider__company_name__icontains=search) |
                Q(content_provider__user__first_name__icontains=search) |
                Q(content_provider__user__last_name__icontains=search)
            )
        # end if

        if date_sort is not None:
            courses = courses.order_by(date_sort)
        # end if

        if price_sort is not None:
            courses = courses.order_by(price_sort)
        # end if

        if rating_sort is not None:
            courses = courses.order_by(rating_sort)
        # end if

        # paginator configs
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        result_page = paginator.paginate_queryset(courses.all(), request)
        serializer = CourseSerializer(result_page, many=True, context={"request": request})

        return paginator.get_paginated_response(serializer.data)
    # end if

    '''
    Create a new Course
    '''
    if request.method == 'POST':
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(user=user)
            data = request.data

            # print(type(json.loads(data['list'])))

            course = Course(
                title=data['title'],
                learning_objectives=json.loads(data['learning_objectives']),
                requirements=json.loads(data['requirements']),
                description=data['description'],
                introduction_video_url=data['introduction_video_url'],
                thumbnail=data['thumbnail'],
                coding_languages=json.loads(data['coding_languages']),
                languages=json.loads(data['languages']),
                categories=json.loads(data['categories']),
                price=data['price'],
                content_provider=content_provider
            )
            course.save()

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, KeyError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def single_course_view(request, pk):
    '''
    Get single course details
    '''
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=pk)
            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Update a course
    '''
    if request.method == 'PUT':
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.content_provider != content_provider:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            data = request.data
            
            course.title=data['title']
            course.learning_objectives=json.loads(data['learning_objectives'])
            course.requirements=json.loads(data['requirements'])
            course.description=data['description']
            course.introduction_video_url=data['introduction_video_url']
            course.thumbnail=data['thumbnail']
            course.coding_languages=json.loads(data['coding_languages'])
            course.languages=json.loads(data['languages'])
            course.categories=json.loads(data['categories'])
            course.price=data['price']
            course.save() # save course

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if 
# end def

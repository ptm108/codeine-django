from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)

import json

from .models import Course, Quiz, Enrollment
from .serializers import CourseSerializer, QuizSerializer
from common.models import Partner, Member


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def course_view(request):
    '''
    Get/ Search all courses
    Params: search, sort
    '''
    if request.method == 'GET':
        try:
            # extract query params
            search = request.query_params.get('search', None)
            date_sort = request.query_params.get('sortDate', None)
            rating_sort = request.query_params.get('sortRating', None)
            partner_id = request.query_params.get('partnerId', None)

            # get pagination params from request, default is (10, 1)
            page_size = int(request.query_params.get('pageSize', 10))

            courses = Course.objects

            if search is not None:
                courses = courses.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(coding_languages__icontains=search) |
                    Q(categories__icontains=search) |
                    Q(partner__organization__organization_name__icontains=search) |
                    Q(partner__user__first_name__icontains=search) |
                    Q(partner__user__last_name__icontains=search)
                )
            if partner_id is not None:
                partner = Partner.objects.get(pk=partner_id)
                courses = courses.filter(partner=partner) # get partner courses
            if date_sort is not None:
                courses = courses.order_by(date_sort)
            if rating_sort is not None:
                courses = courses.order_by(rating_sort)
            # end if

            # paginator configs
            paginator = PageNumberPagination()
            paginator.page_size = page_size

            result_page = paginator.paginate_queryset(courses.all(), request)
            serializer = CourseSerializer(result_page, many=True, context={"request": request})

            return paginator.get_paginated_response(serializer.data)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Partner.DoesNotExist:
            return Response('Invalid partner id', status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
  # end def

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def single_course_view(request, course_id):
    user = request.user

    '''
    Get single course details
    '''
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)

            member = Member.objects.filter(user=user).first()
            
            if member is None: 
                serializer = CourseSerializer(course, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            # end if

            enrollment = Enrollment.objects.filter(member=member).filter(course=course)
            serializer = CourseSerializer(course, context={'request': request, 'member_enrolled': enrollment.exists()})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

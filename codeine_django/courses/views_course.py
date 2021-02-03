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
from .models import Course, Section, Chapter
from .serializers import CourseSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
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
# end def

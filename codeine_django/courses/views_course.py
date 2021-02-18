from django.utils import timezone
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

import json

from .models import Course, Quiz
from .serializers import CourseSerializer, QuizSerializer
from common.models import Partner
from common.permissions import IsPartnerOrReadOnly, IsPartnerOnly


@api_view(['GET', 'POST'])
@permission_classes((IsPartnerOrReadOnly,))
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

            # get pagination params from request, default is (10, 1)
            page_size = int(request.query_params.get('pageSize', 10))

            courses = Course.objects.filter(is_deleted=False).filter(is_available=True).filter(is_published=True)  # implicit requirements for public view

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
            # end if

            if date_sort is not None:
                courses = courses.order_by(date_sort)
            # end if

            if rating_sort is not None:
                courses = courses.order_by(rating_sort)
            # end if

            # paginator configs
            paginator = PageNumberPagination()
            paginator.page_size = page_size

            result_page = paginator.paginate_queryset(courses.all(), request)
            serializer = CourseSerializer(result_page, many=True, context={"request": request, 'public': True})

            return paginator.get_paginated_response(serializer.data)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Create a new Course
    '''
    if request.method == 'POST':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)
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
                partner=partner
            )
            course.save()

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsPartnerOrReadOnly,))
def single_course_view(request, pk):
    '''
    Get single course details
    '''
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=pk)
            return Response(CourseSerializer(course, context={'request': request, 'public': True}).data, status=status.HTTP_200_OK)
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
            partner = Partner.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.partner != partner:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            data = request.data

            course.title = data['title']
            course.learning_objectives = json.loads(data['learning_objectives'])
            course.requirements = json.loads(data['requirements'])
            course.description = data['description']
            course.introduction_video_url = data['introduction_video_url']
            course.coding_languages = json.loads(data['coding_languages'])
            course.languages = json.loads(data['languages'])
            course.categories = json.loads(data['categories'])
            if 'thumbnail' in data:
                course.thumbnail = data['thumbnail']
            # end if
            course.save()  # save course

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Delete a course
    '''
    if request.method == 'DELETE':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.partner != partner:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            course.is_deleted = True
            course.save()

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def publish_course_view(request, pk):
    '''
    Publish course
    '''
    if request.method == 'PATCH':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.partner != partner:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # end if

            course.is_published = True
            course.published_date = timezone.now()
            course.save()

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def unpublish_course_view(request, pk):
    '''
    Publish course
    '''
    if request.method == 'PATCH':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.partner != partner:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # end if

            course.is_published = False
            course.published_date = None
            course.save()

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['POST'])
@permission_classes((IsPartnerOnly,))
def assessment_view(request, course_id):
    user = request.user
    data = request.data

    '''
    Creates a new chapter quiz, returns a empty quiz object
    '''
    if request.method == 'POST':
        with transaction.atomic():
            try:
                partner = user.partner

                # check if chapter is under a course under the current partner
                course = Course.objects.filter(partner=partner).get(pk=course_id)

                quiz = Quiz(
                    course=course,
                    instructions=data['instructions'],
                    passing_marks=int(data['passing_marks'])
                )
                quiz.save()

                serializer = QuizSerializer(quiz)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except (ValueError, IntegrityError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with

    # end if
# end def


@api_view(['PUT', 'DELETE'])
@permission_classes((IsPartnerOnly,))
def single_assessment_view(request, course_id, assessment_id):
    user = request.user
    data = request.data

    '''
    Updates a new assessment, returns a empty quiz object
    '''
    if request.method == 'PUT':
        with transaction.atomic():
            try:
                partner = user.partner

                # check if chapter is under a course under the current partner
                quiz = Quiz.objects.filter(course__partner=partner).get(pk=assessment_id)

                quiz.passing_marks = int(data['passing_marks'])
                quiz.instructions = data['instructions']
                quiz.save()

                serializer = QuizSerializer(quiz)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except (ValueError, IntegrityError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Deletes assessment
    '''
    if request.method == 'DELETE':
        try:
            partner = user.partner

            # check if chapter is under a course under the current partner
            quiz = Quiz.objects.filter(course__partner=partner).get(pk=assessment_id)

            quiz.delete()

            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def activate_course_view(request, course_id):
    '''
    Admin activate course
    '''
    if request.method == 'PATCH':
        try:
            course = Course.objects.get(pk=course_id)

            course.is_available = True
            course.save()

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsAdminUser,))
def deactivate_course_view(request, course_id):
    '''
    Admin deactivate course
    '''
    if request.method == 'PATCH':
        try:
            course = Course.objects.get(pk=course_id)

            course.is_available = False
            course.save()

            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

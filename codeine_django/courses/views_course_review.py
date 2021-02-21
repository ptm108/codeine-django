from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

from .models import Course, CourseReview
from .serializers import CourseReviewSerializer
from common.models import Member
from common.permissions import IsMemberOrReadOnly


@api_view(['POST', 'GET'])
@permission_classes((IsMemberOrReadOnly,))
def course_review_views(request, course_id):
    '''
    Member creates a new Course Review
    '''
    if request.method == 'POST':
        user = request.user
        data = request.data
        try:
            member = Member.objects.get(user=user)
            course = Course.objects.get(pk=course_id)

            course_review = CourseReview.objects.filter(
                Q(course=course) &
                Q(member=member)
            )

            if course_review.exists():  # already submitted a course review
                return Response(status=status.HTTP_409_CONFLICT)
            # end if

            course_review = CourseReview(
                rating=data['rating'], 
                description=data['description'],
                course=course, 
                member=member)
            course_review.save()

            serializer = CourseReviewSerializer(course_review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response("Invalid member", status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response("Invalid course", status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Gets course reviews for this course
    '''
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)
            course_reviews = CourseReview.objects.filter(course=course)
            
            search = request.query_params.get('search', None)
            course_id = request.query_params.get('course_id', None)
            member_id = request.query_params.get('member_id', None)

            if search is not None:
                course_reviews = course_reviews.filter(
                    Q(rating__icontains=search) |
                    Q(description__icontains=search)
                )
            # end if

            if course_id is not None:
                course_reviews = course_reviews.filter(course__id=course_id)
            # end if

            if member_id is not None:
                course_reviews = course_reviews.filter(member__id=member_id)
            # end if

            serializer = CourseReviewSerializer(course_reviews.all(), many=True, context={"request"})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsMemberOrReadOnly,))
def single_course_review_view(request, course_id, review_id):
    '''
    Get course review by review id
    '''
    if request.method == 'GET':
        try:
            course_review = CourseReview.objects.get(pk=review_id)
            serializer = CourseReviewSerializer(course_review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CourseReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # end if

    '''
    Updates rating and description for Course Review
    '''
    if request.method == 'PUT':
        data = request.data
        try:
            with transaction.atomic():
                course_review = CourseReview.objects.get(pk=review_id)
                member = course_review.member
                user =  request.user
                # assert requesting member editing their own course review
                if member.user != user:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                # end if

                if 'rating' in data:
                    course_review.rating = data['rating']
                if 'description' in data:
                    course_review.description = data['description']
                # end if

                course_review.save()
            # end with

            serializer = CourseReviewSerializer(course_review, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CourseReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a course review
    '''
    if request.method == 'DELETE':
        try:
            course_review = CourseReview.objects.get(pk=review_id)
            member = course_review.member
            user =  request.user
            
            # assert requesting member deleting their own course review
            if member.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            course_review.delete()
            return Response(status=status.HTTP_200_OK)
        except CourseReview.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

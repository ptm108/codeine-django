from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import CourseComment, CourseCommentEngagement, CourseMaterial
from .serializers import NestedCourseCommentSerializer, CourseCommentSerializer
from common.permissions import IsMemberOrPartnerOnly, IsMemberOnly, IsPartnerOnly, IsMemberOrPartnerOrReadOnly


@api_view(['POST', 'GET'])
@permission_classes((IsMemberOrPartnerOrReadOnly,))
def course_comments_view(request, material_id):
    user = request.user

    '''
    Creates a new comment or reply
    Can be Member or Partner
    '''
    if request.method == 'POST':
        data = request.data
        try:
            material = CourseMaterial.objects.get(pk=material_id)
            comment_count = CourseComment.objects.filter(course_material=material).count()
            course_comment = CourseComment(comment=data['comment'], course_material=material, user=user, display_id=comment_count + 1)

            if 'reply_to' in data:
                course_comment.reply_to = CourseComment.objects.get(pk=data['reply_to'])
            # end if
            course_comment.save()

            serializer = NestedCourseCommentSerializer(course_comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValueError, KeyError, IntegrityError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    ''' 
    Gets first 2 levels of comments under course material
    '''
    if request.method == 'GET':
        try:
            material = CourseMaterial.objects.get(pk=material_id)
            course_comments = CourseComment.objects.filter(course_material=material).filter(reply_to=None).all()

            serializer = NestedCourseCommentSerializer(course_comments, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValueError, KeyError, IntegrityError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET', 'DELETE', 'PATCH'])
@permission_classes((IsMemberOrPartnerOrReadOnly,))
def single_course_comment_view(request, comment_id):
    '''
    Get Comment by ID
    '''
    if request.method == 'GET':
        try:
            course_comment = CourseComment.objects.get(pk=comment_id)

            serializer = NestedCourseCommentSerializer(course_comment, context={'request': request, 'recursive': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, KeyError, IntegrityError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Delete Comment by ID
    removes user, changes comment to deleted
    '''
    if request.method == 'DELETE':
        user = request.user
        try:
            course_comment = CourseComment.objects.get(pk=comment_id)

            if course_comment.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            course_comment.user = None
            course_comment.comment = 'deleted'
            course_comment.save()

            serializer = NestedCourseCommentSerializer(course_comment, context={'request': request, 'recursive': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Updates comment by ID
    '''
    if request.method == 'PATCH':
        user = request.user
        data = request.data
        try:
            course_comment = CourseComment.objects.get(pk=comment_id)

            if course_comment.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            course_comment.comment = data['comment']
            course_comment.save()

            serializer = NestedCourseCommentSerializer(course_comment, context={'request': request, 'recursive': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, KeyError, IntegrityError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def pin_comment_view(request, comment_id):
    '''
    Pins comment
    '''
    if request.method == 'PATCH':
        user = request.user
        try:
            course_comment = CourseComment.objects.get(pk=comment_id)

            if course_comment.course_material.chapter.course.partner.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            course_comment.pinned = True
            course_comment.save()

            serializer = NestedCourseCommentSerializer(course_comment, context={'request': request, 'recursive': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
    # end if
# end def

@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def unpin_comment_view(request, comment_id):
    '''
    Pins comment
    '''
    if request.method == 'PATCH':
        user = request.user
        try:
            course_comment = CourseComment.objects.get(pk=comment_id)

            if course_comment.course_material.chapter.course.partner.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            course_comment.pinned = False
            course_comment.save()

            serializer = NestedCourseCommentSerializer(course_comment, context={'request': request, 'recursive': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
    # end if
# end def

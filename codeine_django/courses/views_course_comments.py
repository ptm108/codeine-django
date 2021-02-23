from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

from .models import CourseComment, CourseCommentEngagement, CourseMaterial
from .serializers import NestedCourseCommentSerializer, CourseCommentSerializer
from common.permissions import IsMemberOrPartnerOnly, IsMemberOnly, IsPartnerOnly


@api_view(['POST'])
@permission_classes((IsMemberOrPartnerOnly,))
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
            course_comment = CourseComment(comment=data['comment'], course_material=material, user=user)

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
# end def

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import Q, Sum
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response

from .models import Quiz, QuizResult, QuizAnswer, Enrollment
from .serializers import QuizResultSerializer
from common.models import Member, Partner
from common.permissions import IsMemberOnly


@api_view(['POST'])
@permission_classes((IsMemberOnly,))
def quiz_result_views(request, quiz_id):
    user = request.user

    '''
    Creates a new quiz result 
    '''
    if request.method == 'POST':
        try:
            member = Member.objects.get(user=user)
            quiz = Quiz.objects.get(pk=quiz_id)

            # check if member is enrolled in course
            enrollment = Enrollment.objects.filter(member=member).filter(
                Q(course__assessment=quiz) |
                Q(course__chapters__course_materials__quiz=quiz)
            ).first()
            if enrollment is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # end if

            # check if member has an ongoing attempt (submitted = false)
            quiz_result = QuizResult.objects.filter(
                Q(quiz=quiz) &
                Q(member=member) &
                Q(submitted=False)
            ).first()
            if quiz_result is not None:
                return Response(status=status.HTTP_409_CONFLICT)
            # end if

            quiz_result = QuizResult(member=member, quiz=quiz)
            quiz_result.save()

            for qn in quiz.questions.all():
                qa = QuizAnswer(
                    quiz_result=quiz_result,
                    question=qn,
                    response=None,
                    responses=None
                )
                qa.save()
            # end for

            return Response(QuizResultSerializer(quiz_result).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

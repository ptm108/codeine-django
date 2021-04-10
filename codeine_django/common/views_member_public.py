from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Sum
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import BaseUser, Member, CV
from .serializers import MemberSerializer, NestedBaseUserSerializer, CVSerializer
from achievements.models import MemberAchievement
from achievements.serializers import MemberAchievementSerializer
from courses.models import Enrollment, QuizResult
from courses.serializers import NestedEnrollmentSerializer, QuizResultSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def public_member_course_view(request, pk):
    '''
    Public view to get member's courses
    '''
    if request.method == 'GET':
        try:
            user = None
            member = None

            try:
                user = BaseUser.objects.filter(pk=pk).first()
            except:
                pass
            # end try-except

            if user is None:
                member = Member.objects.get(unique_id=pk)
                user = member.user
            else:
                member = user.member
            # end if-else

            # get all enrollments
            enrollments = Enrollment.objects.filter(member=member)
            serialized_enrollments = NestedEnrollmentSerializer(enrollments.all(), many=True, context={'request': request}).data

            for i, enrollment in enumerate(enrollments.all()):
                course = enrollment.course

                # get quiz result
                quiz_results = QuizResult.objects.filter(member=member).filter(quiz__course=course)
                quiz_result = quiz_results.first()
                if quiz_result is not None:
                    total_score = quiz_results.annotate(total_score=Sum('quiz__question_groups__question_bank__questions__shortanswer__marks') + Sum('quiz__question_groups__question_bank__questions__mcq__marks') + Sum('quiz__question_groups__question_bank__questions__mrq__marks'))[0].total_score
                    serialized_enrollments[i]['quiz_result'] = {'actual_score': quiz_result.score, 'total_score': total_score}
                else:
                    serialized_enrollments[i]['quiz_result'] = None
            # end for

            # get all achievement badges
            achievements = MemberAchievement.objects.filter(member=member)
            serialized_achievements = MemberAchievementSerializer(achievements.all(), many=True, context={'request': request}).data

            # get all cvs
            cvs = CV.objects.filter(member=member)
            serialized_cvs = CVSerializer(cvs.all(), many=True).data

            # member details
            serialized_member = NestedBaseUserSerializer(user, context={'request': request}).data

            return Response({
                'member': serialized_member,
                'courses': serialized_enrollments,
                'achievements': serialized_achievements,
                'cv': serialized_cvs},
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError, ValidationError) as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((AllowAny,))
def check_unique_id_view(request, unique_id):
    '''
    Checks if unique id is taken
    Returns 200 OK if not taken, 409 otherwise
    '''
    if request.method == 'GET':
        unique_id_check = Member.objects.filter(unique_id=unique_id).exists()
        id_check = False

        try:
            id_check = BaseUser.objects.filter(id=unique_id).exists()
        except ValidationError:
            pass
        # end try-except
        
        if unique_id_check or id_check:
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            return Response(status=status.HTTP_200_OK)
        # end if-else
    # end if
# end def

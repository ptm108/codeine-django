from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import Q, Sum
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Quiz, QuizResult, QuizAnswer, Enrollment, Question, ShortAnswer, MRQ, MCQ, CourseMaterial
from .serializers import QuizResultSerializer, NestedQuizResultSerializer
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
                print(quiz_result)
                return Response(QuizResultSerializer(quiz_result).data, status=status.HTTP_202_ACCEPTED)
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


@api_view(['PUT', 'GET'])
@permission_classes((IsAuthenticated,))
def update_quiz_result_view(request, quiz_result_id):
    user = request.user

    '''
    Get QuizResult by id
    '''
    if request.method == 'GET':
        try:
            member = Member.objects.filter(user=user).first()
            partner = Partner.objects.filter(user=user).first()

            quiz_results = QuizResult.objects

            if member is not None:
                quiz_results = quiz_results.filter(member=member)
            elif partner is not None:
                quiz_results = quiz_results.filter(
                    Q(quiz__course__partner=partner) |
                    Q(quiz__course_material__chapter__course__partner=partner)
                )
            # end if-else

            quiz_result = quiz_results.get(pk=quiz_result_id)

            serializer = NestedQuizResultSerializer(quiz_result, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Updates responses in QuizResult
    '''
    if request.method == 'PUT':
        try:
            member = Member.objects.get(user=user)
            quiz_result = QuizResult.objects.filter(member=member).get(pk=quiz_result_id)

            # check if quiz attempt is still ongoing
            if quiz_result.submitted == True:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            # end if

            data = request.data
            quiz_answer = QuizAnswer.objects.filter(quiz_result=quiz_result).get(question__id=data['question'])
            if 'response' in data:
                quiz_answer.response = data['response']
            if 'responses' in data:
                quiz_answer.responses = data['responses']
            # end ifs
            quiz_answer.save()

            return Response(QuizResultSerializer(quiz_result).data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValidationError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsMemberOnly,))
def sumbit_quiz_result_view(request, quiz_result_id):
    user = request.user

    '''
    Marks quiz as submitted and tabulates score
    '''
    if request.method == 'PATCH':
        try:
            member = user.member
            quiz_result = QuizResult.objects.filter(member=member).get(pk=quiz_result_id)
            quiz_answers = quiz_result.quiz_answers

            quiz = quiz_result.quiz

            with transaction.atomic():
                total_marks = ShortAnswer.objects.filter(question__quiz=quiz).aggregate(Sum('marks'))['marks__sum'] if ShortAnswer.objects.filter(question__quiz=quiz).exists() else 0
                total_marks += MRQ.objects.filter(question__quiz=quiz).aggregate(Sum('marks'))['marks__sum'] if MRQ.objects.filter(question__quiz=quiz).exists() else 0
                total_marks += MCQ.objects.filter(question__quiz=quiz).aggregate(Sum('marks'))['marks__sum'] if MCQ.objects.filter(question__quiz=quiz).exists() else 0
                score = 0

                for answer in quiz_answers.all():
                    question = answer.question

                    # evaluate short answer questions
                    try:
                        keywords = question.shortanswer.keywords
                        responses = answer.response.split(' ')
                        responses = [response for response in responses if response in keywords]

                        score += len(responses) / len(keywords) * question.shortanswer.marks
                    except ShortAnswer.DoesNotExist:
                        pass
                    # end try-except

                    # evaluate mcq
                    try:
                        if answer.response == question.mcq.correct_answer:
                            score += question.mcq.marks
                        # end if
                    except MCQ.DoesNotExist:
                        pass
                    # end try-except

                    # evaluate mrq
                    try:
                        correct_answer = question.mrq.correct_answer
                        responses = [response for response in answer.responses if response in correct_answer]

                        score += len(responses) / len(correct_answer) * question.mrq.marks
                    except MRQ.DoesNotExist:
                        pass
                    # end try-except
                # end for

                quiz_result.score = score
                quiz_result.submitted = True

                if score >= quiz.passing_marks:
                    quiz_result.passed = True

                    if quiz.course is not None:  # is assessment
                        course = quiz.course
                        enrollment = Enrollment.objects.filter(course=course).get(member=member)
                        enrollment.materials_done = [str(course_material.id) for course_material in CourseMaterial.objects.filter(chapter__course=course).all()]
                        enrollment.progress = 100
                        enrollment.save()
                    # end if

                # end if
                quiz_result.save()
            # end with

            return Response(QuizResultSerializer(quiz_result).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError, ValidationError, AttributeError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_quiz_results(request):
    user = request.user

    '''
    Gets all quizzes by requesting user type
    '''
    if request.method == 'GET':
        try:
            member = Member.objects.filter(user=user).first()
            partner = Partner.objects.filter(user=user).first()

            quiz_results = QuizResult.objects

            if member is not None:
                quiz_results = quiz_results.filter(member=member)
            elif partner is not None:
                quiz_results = quiz_results.filter(
                    Q(quiz__course__partner=partner) |
                    Q(quiz__course_material__chapter__course__partner=partner)
                )
            # end if-else

            # query params
            course_id = request.query_params.get('course_id', None)
            if course_id is not None:
                quiz_results = quiz_results.filter(
                    Q(quiz__course__id=course_id) |
                    Q(quiz__course_material__chapter__course__id=course_id)
                )
            # end if

            serializer = NestedQuizResultSerializer(quiz_results.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

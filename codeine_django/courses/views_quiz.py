from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

import json

from .models import Quiz, Question, ShortAnswer, MCQ, MRQ
from .serializers import QuizSerializer
from common.permissions import IsPartnerOnly, IsPartnerOrReadOnly


@api_view(['GET'])
@permission_classes((IsPartnerOnly,))
def quiz_view(request, quiz_id):
    user = request.user

    '''
    Get a quiz by id
    '''
    if request.method == 'GET':
        try:
            partner = user.partner

            # check if partner is owner of course/material
            quiz = Quiz.objects.filter(
                Q(course__partner=partner) |
                Q(course_material__chapter__course__partner=partner)
            ).get(pk=quiz_id)

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


@api_view(['POST'])
@permission_classes((IsPartnerOnly,))
def add_question_view(request, quiz_id):
    user = request.user
    data = request.data

    '''
    Adds new question to quiz
    '''
    if request.method == 'POST':
        with transaction.atomic():

            try:
                partner = user.partner

                qn_type = request.query_params.get('type', None)
                if qn_type is None:
                    return Response('Type not specified', status=status.HTTP_400_BAD_REQUEST)
                # end if

                # check if partner is owner of course/material
                quiz = Quiz.objects.filter(
                    Q(course__partner=partner) |
                    Q(course_material__chapter__course__partner=partner)
                ).get(pk=quiz_id)

                question = Question(
                    title=data['title'],
                    subtitle=data['subtitle'] if 'subtitle' in data else None,
                    order=quiz.questions.count() + 1,
                    quiz=quiz
                )
                question.save()

                if qn_type == 'shortanswer':
                    sa = ShortAnswer(
                        question=question,
                        marks=int(data['marks']),
                        keywords=data['keywords'] if type(data['keywords']) is list else None
                    )
                    sa.save()
                if qn_type == 'mcq':
                    print(type(data['options']))
                    mcq = MCQ(
                        question=question,
                        marks=int(data['marks']),
                        options=data['options'] if type(data['options']) is list else None,
                        correct_answer=data['correct_answer']
                    )
                    mcq.save()
                if qn_type == 'mrq':
                    mrq = MRQ(
                        question=question,
                        marks=int(data['marks']),
                        options=data['options'] if type(data['options']) is list else None,
                        correct_answer=data['correct_answer'] if type(data['correct_answer']) is list else None
                    )
                    mrq.save()
                # end ifs

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
def single_question_view(request, quiz_id, question_id):
    user = request.user

    '''
    Update a question
    '''
    if request.method == 'PUT':
        data = request.data

        with transaction.atomic():
            try:
                partner = user.partner

                # check if partner is owner of course/material
                question = Question.objects.filter(
                    Q(quiz__course__partner=partner) |
                    Q(quiz__course_material__chapter__course__partner=partner)
                ).get(pk=question_id)
                quiz = question.quiz

                qn_type = request.query_params.get('type', None)
                if qn_type is None:
                    return Response('Type not specified', status=status.HTTP_400_BAD_REQUEST)
                # end if

                question.title = data['title']
                question.subtitle = data['subtitle'] if 'subtitle' in data else None
                question.save()

                if qn_type == 'shortanswer':
                    sa = question.shortanswer
                    sa.question = question
                    sa.marks = int(data['marks'])
                    sa.keywords = data['keywords'] if type(data['keywords']) is list else None
                    sa.save()
                if qn_type == 'mcq':
                    mcq = question.mcq
                    mcq.question = question
                    mcq.marks = int(data['marks'])
                    mcq.options = data['options'] if type(data['options']) is list else None
                    mcq.correct_answer = data['correct_answer']
                    mcq.save()
                if qn_type == 'mrq':
                    mrq = question.mrq
                    mrq.question = question
                    mrq.marks = int(data['marks'])
                    mrq.options = data['options'] if type(data['options']) is list else None
                    mrq.correct_answer = data['correct_answer'] if type(data['correct_answer']) is list else None
                    mrq.save()
                # end ifs

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
    Deletes the question by id
    '''
    if request.method == 'DELETE':
        try:
            partner = user.partner

            # check if partner is owner of course/material
            question = Question.objects.filter(
                Q(quiz__course__partner=partner) |
                Q(quiz__course_material__chapter__course__partner=partner)
            ).get(pk=question_id)
            quiz = question.quiz

            question.delete()

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
@permission_classes((IsPartnerOnly,))
def order_question_view(request, quiz_id):
    user = request.user

    '''
    Sets the order of questions by list of question ids
    '''
    if request.method == 'PATCH':
        try:
            partner = user.partner

            # check if partner is owner of course/material
            quiz = Quiz.objects.filter(
                Q(course__partner=partner) |
                Q(course_material__chapter__course__partner=partner)
            ).get(pk=quiz_id)

            question_id_list = request.data

            for index, qn_id in enumerate(question_id_list):
                Question.objects.filter(pk=qn_id).update(order=index + 1)
            # end for

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


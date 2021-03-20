from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

import json

from .models import Quiz, Question, ShortAnswer, MCQ, MRQ, QuestionGroup
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

            serializer = QuizSerializer(quiz, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['POST'])
@permission_classes((IsPartnerOnly,))
@parser_classes([MultiPartParser, FormParser])
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
                    quiz=quiz,
                    image=data['image'] if 'image' in data else None,
                    group=None,
                )
                question.save()

                # adds a question to a group
                if 'label' in data:
                    question_group = QuestionGroup.objects.filter(Q(quiz=quiz) & Q(label=data['label'])).first()
                    if question_group is None:
                        question_group = QuestionGroup(quiz=quiz, label=data['label'])
                        question_group.save()
                    # end if
                    question.group = question_group
                    question.save()
                # end if

                if qn_type == 'shortanswer':
                    sa = ShortAnswer(
                        question=question,
                        marks=int(data['marks']),
                        keywords=json.loads(data['keywords']) if 'keywords' in data else None
                    )
                    sa.save()
                if qn_type == 'mcq':
                    print(type(json.loads(data['options'])))
                    mcq = MCQ(
                        question=question,
                        marks=int(data['marks']),
                        options=json.loads(data['options']) if 'options' in data else None,
                        correct_answer=data['correct_answer']
                    )
                    mcq.save()
                if qn_type == 'mrq':
                    mrq = MRQ(
                        question=question,
                        marks=int(data['marks']),
                        options=json.loads(data['options']) if 'options' in data else None,
                        correct_answer=json.loads(data['correct_answer']) if 'correct_answer' in data else None
                    )
                    mrq.save()
                # end ifs

                serializer = QuizSerializer(quiz, context={'request': request})
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
@parser_classes([MultiPartParser, FormParser])
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

                question.title = data['title'] if 'title' in data else question.title
                question.subtitle = data['subtitle'] if 'subtitle' in data else question.subtitle
                question.image = data['image'] if 'image' in data else question.image

                # adds the question to a group
                if 'label' in data:
                    question_group = QuestionGroup.objects.filter(Q(quiz=quiz) & Q(label=data['label'])).first()
                    if question_group is None:
                        question_group = QuestionGroup(quiz=quiz, label=data['label'])
                        question_group.save()
                    # end if
                    question.group = question_group
                    question.save()
                # end if
                question.save()

                if qn_type == 'shortanswer':
                    sa = question.shortanswer
                    sa.question = question
                    sa.marks = int(data['marks'])
                    sa.keywords = json.loads(data['keywords']) if 'keywords' in data else sa.keywords
                    sa.save()
                if qn_type == 'mcq':
                    mcq = question.mcq
                    mcq.question = question
                    mcq.marks = int(data['marks'])
                    mcq.options = json.loads(data['options']) if 'options' in data else mcq.options,
                    mcq.correct_answer = data['correct_answer']
                    mcq.save()
                if qn_type == 'mrq':
                    mrq = question.mrq
                    mrq.question = question
                    mrq.marks = int(data['marks'])
                    mrq.options = json.loads(data['options']) if 'options' in data else mrq.options,
                    mrq.correct_answer = json.loads(data['correct_answer']) if 'correct_answer' in data else mrq.correct_answer
                    mrq.save()
                # end ifs

                serializer = QuizSerializer(quiz, context={'request': request})
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

            serializer = QuizSerializer(quiz, context={'request': request})
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

            serializer = QuizSerializer(quiz, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsPartnerOnly,))
def all_quiz_view(request):
    user = request.user

    '''
    Get Quizzes under Partner
    '''
    if request.method == 'GET':
        try:
            partner = user.partner

            # check if partner is owner of course/material
            quiz = Quiz.objects.filter(
                Q(course__partner=partner) |
                Q(course_material__chapter__course__partner=partner)
            )

            course_id = request.query_params.get('course_id', None)
            if course_id is not None:
                quiz = quiz.filter(
                    Q(course__id=course_id) |
                    Q(course_material__chapter__course__id=course_id)
                )
            # end if

            serializer = QuizSerializer(quiz, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

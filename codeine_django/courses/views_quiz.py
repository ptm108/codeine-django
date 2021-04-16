from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

import json

from .models import Quiz, Question, ShortAnswer, MCQ, MRQ, QuestionGroup, Course, QuestionBank
from .serializers import QuizSerializer, QuestionBankSerializer
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
def add_question_view(request, qb_id):
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
                question_bank = QuestionBank.objects.filter(course__partner=partner).get(pk=qb_id)
                course = question_bank.course

                question = Question(
                    title=data['title'],
                    subtitle=data['subtitle'] if 'subtitle' in data else None,
                    order=question_bank.questions.count() + 1,
                    question_bank=question_bank,
                    image=data['image'] if 'image' in data else None,
                )
                question.save()

                if qn_type == 'shortanswer':
                    sa = ShortAnswer(
                        question=question,
                        marks=int(data['marks']),
                        keywords=json.loads(data['keywords']) if 'keywords' in data else None
                    )
                    sa.save()
                if qn_type == 'mcq':
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
                question_banks = QuestionBank.objects.filter(course=course)

                serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
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
def single_question_view(request, qb_id, question_id):
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
                    Q(question_bank__course__partner=partner)
                ).get(pk=question_id)
                question_bank = question.question_bank

                qn_type = request.query_params.get('type', None)
                if qn_type is None:
                    return Response('Type not specified', status=status.HTTP_400_BAD_REQUEST)
                # end if

                question.title = data['title'] if 'title' in data else question.title
                question.subtitle = data['subtitle'] if 'subtitle' in data else question.subtitle
                question.image = data['image'] if 'image' in data else question.image

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
                    mcq.options = json.loads(data['options']) if 'options' in data else mcq.options
                    mcq.correct_answer = data['correct_answer']
                    mcq.save()
                if qn_type == 'mrq':
                    mrq = question.mrq
                    mrq.question = question
                    mrq.marks = int(data['marks'])
                    mrq.options = json.loads(data['options']) if 'options' in data else mrq.options
                    mrq.correct_answer = json.loads(data['correct_answer']) if 'correct_answer' in data else mrq.correct_answer
                    mrq.save()
                # end ifs
                question_banks = QuestionBank.objects.filter(course=question_bank.course)

                serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
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
                Q(question_bank__course__partner=partner)
            ).get(pk=question_id)
            question.delete()

            question_bank = question.question_bank
            question_banks = QuestionBank.objects.filter(course=question_bank.course)

            serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
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
def order_question_view(request, qb_id):
    user = request.user

    '''
    Sets the order of questions by list of question ids
    '''
    if request.method == 'PATCH':
        try:
            partner = user.partner

            # check if partner is owner of course/material
            question_bank = QuestionBank.objects.filter(course__partner=partner).get(pk=qb_id)

            question_id_list = request.data

            for index, qn_id in enumerate(question_id_list):
                Question.objects.filter(pk=qn_id).update(order=index + 1)
            # end for

            question_banks = QuestionBank.objects.filter(course=question_bank.course)

            serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
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


@api_view(['GET', 'POST', 'PUT'])
@permission_classes((IsPartnerOnly,))
def question_bank_view(request, course_id):
    user = request.user
    data = request.data

    '''
    Gets all question banks in a course
    '''
    if request.method == 'GET':
        try:
            partner = user.partner
            course = Course.objects.filter(partner=partner).get(pk=course_id)
            question_banks = QuestionBank.objects.filter(course=course)

            serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Creates a question bank, otherwise if exists, updates question bank
    Returns list of question banks
    '''
    if request.method == 'POST':
        try:
            partner = user.partner
            course = Course.objects.filter(partner=partner).get(pk=course_id)

            QuestionBank(
                label=data['label'],
                course=course
            ).save()
            question_banks = QuestionBank.objects.filter(course=course)

            serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print(e)
            return Response(status=status.HTTP_409_CONFLICT)
        # end try-except
    # end if

    '''
    Imports a question bank .json file
    Adds the question bank to the course
    '''
    if request.method == 'PUT':
        try:
            partner = user.partner
            course = Course.objects.filter(partner=partner).get(pk=course_id)

            qb = QuestionBank.objects.get(pk=data['id'])

            with transaction.atomic():
                qb.id = None
                qb.label = data['label']
                qb.course = course
                qb.save()

                for qn in data['questions']:
                    question = Question.objects.get(pk=qn['id'])
                    question.id = None
                    question.question_bank = qb
                    question.save()

                    if qn['mcq'] is not None:
                        mcq = MCQ(
                            question=question,
                            marks=qn['mcq']['marks'],
                            options=qn['mcq']['options'],
                            correct_answer=qn['mcq']['correct_answer']
                        )
                        mcq.save()
                    elif qn['mrq'] is not None:
                        mrq = MRQ(
                            question=question,
                            marks=qn['mrq']['marks'],
                            options=qn['mrq']['options'],
                            correct_answer=qn['mrq']['correct_answer']
                        )
                        mrq.save()
                    elif qn['shortanswer'] is not None:
                        sa = ShortAnswer(
                            question=question,
                            marks=qn['shortanswer']['marks'],
                            keywords=qn['shortanswer']['keywords']
                        )
                        sa.save()
                    # end if-else
                # end for
            # end with

            question_banks = QuestionBank.objects.filter(course=course)

            serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print(e)
            return Response(status=status.HTTP_409_CONFLICT)
        # end try-except
    # end if
# end def


@api_view(['PUT', 'DELETE'])
@permission_classes((IsPartnerOnly,))
def single_question_bank_view(request, course_id, qb_id):
    user = request.user
    data = request.data

    '''
    Updates a question bank
    '''
    if request.method == 'PUT':
        try:
            partner = user.partner
            course = Course.objects.filter(partner=partner).get(pk=course_id)
            question_bank = QuestionBank.objects.filter(course=course).get(pk=qb_id)

            question_bank.label = data['label']
            question_bank.save()

            question_banks = QuestionBank.objects.filter(course=course)

            serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Delete a question bank
    Returns list of question banks
    '''
    if request.method == 'DELETE':
        try:
            partner = user.partner
            course = Course.objects.filter(partner=partner).get(pk=course_id)
            question_bank = QuestionBank.objects.filter(course=course).get(pk=qb_id)
            question_bank.delete()

            question_banks = QuestionBank.objects.filter(course=course)

            serializer = QuestionBankSerializer(question_banks.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PUT', 'DELETE'])
@permission_classes((IsPartnerOnly,))
def question_group_view(request, quiz_id):
    user = request.user
    data = request.data

    '''
    Add a question bank to the quiz
    returns update quiz
    '''
    if request.method == 'PUT':
        try:
            partner = user.partner
            quiz = Quiz.objects.filter(
                Q(course__partner=partner) |
                Q(course_material__chapter__course__partner=partner)
            ).get(pk=quiz_id)
            course = Course.objects.filter(
                Q(assessment__id=quiz_id) |
                Q(chapters__course_materials__quiz__id=quiz_id)
            ).first()

            question_bank = QuestionBank.objects.filter(course=course).get(pk=data['qb_id'])
            question_group = QuestionGroup.objects.filter(Q(quiz=quiz) & Q(question_bank=question_bank)).first()

            if question_group is None:
                QuestionGroup(
                    count=data['count'],
                    order=quiz.question_groups.count() + 1,
                    quiz=quiz,
                    question_bank=question_bank
                ).save()
            else:
                question_group.count = data['count']
                question_group.save()
            # end if-else

            quiz = Quiz.objects.get(pk=quiz_id)
            serializer = QuizSerializer(quiz, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Delete a question group
    returns updated quiz
    '''
    if request.method == 'DELETE':
        # print(data)
        try:
            partner = user.partner
            quiz = Quiz.objects.filter(
                Q(course__partner=partner) |
                Q(course_material__chapter__course__partner=partner)
            ).get(pk=quiz_id)
            course = Course.objects.filter(
                Q(assessment__id=quiz_id) |
                Q(chapters__course_materials__quiz__id=quiz_id)
            ).first()

            question_bank = QuestionBank.objects.filter(course=course).get(pk=data['qb_id'])

            question_group = QuestionGroup.objects.filter(Q(quiz=quiz) & Q(question_bank=question_bank)).first()
            question_group.delete()

            quiz = Quiz.objects.get(pk=quiz_id)
            serializer = QuizSerializer(quiz, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, IntegrityError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
# end def

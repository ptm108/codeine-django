from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Chapter, CourseMaterial, CourseFile, Video
from .serializers import CourseSerializer, CourseMaterialSerializer

from common.permissions import IsPartnerOnly, IsPartnerOrReadOnly


@api_view(['POST'])
@permission_classes((IsPartnerOnly,))
@parser_classes([MultiPartParser, FormParser])
def file_views(request, chapter_id):
    user = request.user
    data = request.data

    '''
    Creates a new course material (type = file)
    '''
    if request.method == 'POST':
        with transaction.atomic():
            try:
                partner = user.partner

                # check if chapter is under a course under the current partner
                chapter = Chapter.objects.filter(course__partner=partner).get(pk=chapter_id)
                course = chapter.course

                if 'zip_file' not in data and 'google_drive_url' not in data:
                    return Response('No file uploaded', status=status.HTTP_400_BAD_REQUEST)
                # end if

                course_material = CourseMaterial(
                    title=data['title'],
                    description=data['description'],
                    material_type='FILE',
                    order=chapter.course_materials.count(),
                    chapter=chapter,
                )
                course_material.save()

                course_file = CourseFile(
                    course_material=course_material,
                    zip_file=data['zip_file'] if 'zip_file' in data else None,
                    google_drive_url=data['googe_drive_url'] if 'google_drive_url' in data else None
                )
                course_file.save()

                serializer = CourseSerializer(course, context={'request': request, 'public': False})
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


@api_view(['PUT'])
@permission_classes((IsPartnerOnly,))
@parser_classes([MultiPartParser, FormParser])
def update_file_view(request, material_id):
    user = request.user
    data = request.data

    '''
    Updates a new course material (type = file)
    '''
    if request.method == 'PUT':
        with transaction.atomic():
            try:
                partner = user.partner

                # check if chapter is under a course under the current partner
                course_material = CourseMaterial.objects.filter(chapter__course__partner=partner).get(pk=material_id)
                course = course_material.chapter.course

                if 'zip_file' not in data and 'google_drive_url' not in data:
                    return Response('No file uploaded', status=status.HTTP_400_BAD_REQUEST)
                # end if

                course_material.title = data['title']
                course_material.description = data['description']
                course_material.save()

                course_file = course_material.course_file
                course_file.zip_file = data['zip_file'] if 'zip_file' in data else None
                course_file.google_drive_url = data['google_drive_url'] if 'google_drive_url' in data else None
                course_file.save()

                serializer = CourseSerializer(course, context={'request': request, 'public': False})
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


@api_view(['POST'])
@permission_classes((IsPartnerOnly,))
def video_views(request, chapter_id):
    user = request.user
    data = request.data

    '''
    Creates a new course material (type = video)
    '''
    if request.method == 'POST':
        with transaction.atomic():
            try:
                partner = user.partner

                # check if chapter is under a course under the current partner
                chapter = Chapter.objects.filter(course__partner=partner).get(pk=chapter_id)
                course = chapter.course

                if 'video_url' not in data:
                    return Response('No video uploaded', status=status.HTTP_400_BAD_REQUEST)
                # end if

                course_material = CourseMaterial(
                    title=data['title'],
                    description=data['description'],
                    material_type='VIDEO',
                    order=chapter.course_materials.count(),
                    chapter=chapter,
                )
                course_material.save()

                video = Video(
                    course_material=course_material,
                    video_url=data['video_url']
                )
                video.save()

                serializer = CourseSerializer(course, context={'request': request, 'public': False})
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


@api_view(['PUT'])
@permission_classes((IsPartnerOnly,))
def update_video_view(request, material_id):
    user = request.user
    data = request.data

    '''
    Updates a new course material (type = video)
    '''
    if request.method == 'PUT':
        with transaction.atomic():
            try:
                partner = user.partner

                # check if chapter is under a course under the current partner
                course_material = CourseMaterial.objects.filter(chapter__course__partner=partner).get(pk=material_id)
                course = course_material.chapter.course

                if 'video_url' not in data:
                    return Response('No video uploaded', status=status.HTTP_400_BAD_REQUEST)
                # end if

                course_material.title = data['title']
                course_material.description = data['description']
                course_material.save()

                course_file = course_material.video
                course_file.video_url = data['video_url']
                course_file.save()

                serializer = CourseSerializer(course, context={'request': request, 'public': False})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist as e:
                print(e)
                return Response(status=status.HTTP_404_NOT_FOUND)
            except (ValueError, IntegrityError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsPartnerOnly,))
def order_material_view(request, chapter_id):
    user = request.user

    '''
    Updates order of course materials by array of ids
    '''
    if request.method == 'PATCH':
        try:
            partner = user.partner

            # check if chapter is under a course under the current partner
            chapter = Chapter.objects.filter(course__partner=partner).get(pk=chapter_id)
            course = chapter.course

            material_id_list = request.data

            for index, material_id in enumerate(material_id_list):
                CourseMaterial.objects.filter(pk=material_id).update(order=index)
            # end for

            serializer = CourseSerializer(course, context={'request': request, 'public': False})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

# end def


@api_view(['GET', 'DELETE'])
@permission_classes((IsPartnerOnly,))
def single_material_view(request, material_id):
    user = request.user

    '''
    Get course material by id
    '''
    if request.method == 'GET':
        try:
            partner = user.partner

            # check if chapter is under a course under the current partner
            course_material = CourseMaterial.objects.filter(chapter__course__partner=partner).get(pk=material_id)

            serializer = CourseMaterialSerializer(course_material, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except

    # end if

    '''
    Delete Course Material by id
    '''
    if request.method == 'DELETE':
        try:
            partner = user.partner

            # check if chapter is under a course under the current partner
            course_material = CourseMaterial.objects.filter(chapter__course__partner=partner).get(pk=material_id)
            course = course_material.chapter.course

            course_material.delete()

            serializer = CourseSerializer(course, context={'request': request, 'public': False})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Course, Chapter
from .serializers import CourseSerializer, ChapterSerializer

from common.models import ContentProvider
from common.permissions import IsContentProviderOnly, IsContentProviderOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes((IsContentProviderOnly,))
def chapter_view(request, pk):
    '''
    Get all chapters under Course(pk=pk)
    '''
    if request.method == 'GET':
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.content_provider != content_provider:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            chapters = Chapter.objects.filter(course=course)
            serializer = ChapterSerializer(chapters, many=True, context={'public': False})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Creates a new chapter 
    Adds chapter to course(pk=pk)
    '''
    if request.method == 'POST':
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.content_provider != content_provider:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            data = request.data

            chapter = Chapter(
                title=data['title'],
                overview=data['overview'],
                order=int(data['order']),
                course=course
            )
            chapter.save()

            serializer = ChapterSerializer(chapter, context={'public': True})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsContentProviderOnly,))
def single_chapter_view(request, pk, chapter_id):
    '''
    GET a single chapter in a course 
    '''
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=pk)
            chapter = Chapter.objects.filter(course=course).get(pk=chapter_id)

            serializer = ChapterSerializer(chapter, context={'public': True})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Chapter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Edits a chapter
    '''
    if request.method == 'PUT':
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.content_provider != content_provider:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            chapter = Chapter.objects.filter(course=course).get(pk=chapter_id)
            data = request.data

            chapter.title = data['title']
            chapter.overview = data['overview']
            chapter.save()

            serializer = ChapterSerializer(chapter, context={'public': True})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a chapter
    '''
    if request.method == 'DELETE':
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.content_provider != content_provider:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            chapter = Chapter.objects.filter(course=course).get(pk=chapter_id)
            chapter.delete()

            serializer = ChapterSerializer(chapter, context={'public': True})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsContentProviderOnly,))
def order_chapter_view(request, pk):
    '''
    Updates order of chapters by array of chapter ids
    '''
    if request.method == 'PATCH':
        try:
            user = request.user
            content_provider = ContentProvider.objects.get(user=user)

            course = Course.objects.get(pk=pk)

            # check if content provider is owner of course
            if course.content_provider != content_provider:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if

            chapter_id_list = request.data

            for index, chapter_id in enumerate(chapter_id_list):
                Chapter.objects.filter(pk=chapter_id).update(order=index)
            # end for

            serializer = CourseSerializer(course, context={'request': request, 'public': True})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

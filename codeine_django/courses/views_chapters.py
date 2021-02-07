from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)

from .models import Course, Chapter
from .serializers import ChapterSerializer

from common.models import ContentProvider
from common.permissions import IsContentProviderOnly, IsContentProviderOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes((IsContentProviderOnly,))
def chapter_views(request, pk):
    '''
    Get all chapters under Course(pk=pk)
    '''
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=pk)

            chapters = Chapter.objects.get(course=course)
            serializer = ChapterSerializer(chapters, many=True, context={'public': False})
            return Response()
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
                description=data['overview'],
                order=data['order'],
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

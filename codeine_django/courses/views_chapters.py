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


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
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
# end def

from .models import Achievement
from .serializer import AchievementSerializer
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

@api_view(['GET', 'POST'])
@permission_classes((IsAdminUser,))
@parser_classes((MultiPartParser, FormParser))
def achievement_view(request):

    '''
    Get all Achievements
    '''
    if request.method == 'GET':
        try:
            achievements = Achievement.objects

            # extract query params
            title = request.query_params.get('title', None)
            
            if title is not None:
                achievements = achievements.filter(
                    Q(title__icontains=title) 
                )
            # end if

            serializer = AchievementSerializer(achievements.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Create a new Achievement
    '''
    if request.method == 'POST':
        try:
            data = request.data

            achievement = Achievement(
                title=data['title'],
                badge=data['badge'],
            )
            achievement.save()

            return Response(AchievementSerializer(achievement, context={'request': request}).data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes((IsAdminUser,))
@parser_classes((MultiPartParser, FormParser))
def single_achievement_view(request, pk):

    '''
    Get Achievement by ID
    '''
    if request.method == 'GET':
        try:
            achievement = Achievement.objects.get(pk=pk)

            serializer = AchievementSerializer(achievement, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

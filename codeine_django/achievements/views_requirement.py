from .models import Achievement, AchievementRequirement
from .serializer import AchievementRequirementSerializer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser,
)

@api_view(['GET', 'POST'])
@permission_classes((IsAdminUser,))
def achievement_requirement_view(request, pk):
    '''
    Get all Achievement Requirements by Achievement 
    '''
    if request.method == 'GET':
        try:
            achievement = Achievement.objects.get(pk=pk)
            requirements = AchievementRequirement.objects.filter(achievement=achievement)

            serializer = AchievementRequirementSerializer(requirements, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Create a new Achievement Requirement
    '''
    if request.method == 'POST':
        try:
            data = request.data

            achievement = Achievement.objects.get(pk=pk)
            requirement = AchievementRequirement(
                category = data['category'],
                coding_languages = data['coding_languages'],
                experience_point = data['experience_point'],
                achievement=achievement
            )
            requirement.save()

            return Response(AchievementRequirementSerializer(requirement, context={'request': request}).data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


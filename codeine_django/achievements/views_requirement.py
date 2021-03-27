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


@api_view(['GET', 'POST', 'DELETE'])
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
            print(data['stat'])

            achievement = Achievement.objects.get(pk=pk)
            stat = data['stat']
            if stat == 'Machine Learning':
                stat = 'ML'
            if stat == 'Database Administration':
                stat = 'DB'
            if stat == 'Security':
                stat = 'SEC'
            if stat == 'UI/UX':
                stat = 'UI'
            if stat == 'Frontend':
                stat =  "FE"
            if stat == 'Backend':
                stat = 'BE'
            if stat == 'Python':
                stat = 'PY'
            if stat == 'Java':
                stat = 'JAVA'
            if stat == 'Javascript':
                stat = 'JS'
            if stat == 'C++':
                stat = 'CPP'
            if stat == 'C#':
                stat = 'CS'
            if stat == 'Ruby':
                stat = 'RUBY'

            requirement = AchievementRequirement(
                stat = stat,
                experience_point = data['experience_point'],
                achievement=achievement
            )
            requirement.save()
            print(requirement)

            return Response(AchievementRequirementSerializer(requirement, context={'request': request}).data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Delete all Achievement Requirements by Achievement 
    '''
    if request.method == 'DELETE':
        try:
            achievement = Achievement.objects.get(pk=pk)
            requirements = AchievementRequirement.objects.filter(achievement=achievement)

            requirements.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes((IsAdminUser,))
def single_achievement_requirement_view(request, pk, req_id):

    '''
    Get Achievement Requirement by ID
    '''
    if request.method == 'GET':
        try:
            requirement = AchievementRequirement.objects.get(pk=req_id)

            serializer = AchievementRequirementSerializer(requirement, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Update an Achievement Requirement
    '''
    if request.method == 'PATCH':
        try:
            requirement = AchievementRequirement.objects.get(pk=req_id)
            data = request.data

            if 'stat' in data:
                requirement.category=data['stat']
            if 'experience_point' in data:
                requirement.experience_point=data['experience_point']
            # end if 

            requirement.save() 

            serializer = AchievementRequirementSerializer(requirement, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Delete an Achievement
    '''
    if request.method == 'DELETE':
        try:
            requirement = AchievementRequirement.objects.get(pk=req_id)

            requirement.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

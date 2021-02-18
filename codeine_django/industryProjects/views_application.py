from .models import IndustryProject, IndustryProjectApplication
from .serializers import IndustryProjectApplicationSerializer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from common.models import Member
from common.permissions import IsPartnerOnly, IsMemberOrReadOnly

@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def application_view(request, pk):
    '''
    Get all Applications by Industry Project ID
    '''
    if request.method == 'GET':
        try:
            industry_project = IndustryProject.objects.get(pk=pk)
            applications = IndustryProjectApplication.objects.filter(industry_project=industry_project)

            serializer = IndustryProjectApplicationSerializer(applications, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Create a new Application
    '''
    if request.method == 'POST':
        try:
            user = request.user
            member = Member.objects.get(user=user)
            industry_project = IndustryProject.objects.get(pk=pk)

            application = IndustryProjectApplication(     
                member = member,
                industry_project = industry_project
            )
            application.save()

            serializer = IndustryProjectApplicationSerializer(application, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def



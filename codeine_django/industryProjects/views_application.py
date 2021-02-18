from .models import IndustryProject, IndustryProjectApplication
from .serializers import IndustryProjectApplicationSerializer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from common.models import Member
from common.permissions import IsPartnerOrReadOnly, IsMemberOrReadOnly

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

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsPartnerOrReadOnly,))
def single_application_view(request, pk, app_id):

    '''
    Get Application by ID
    '''
    if request.method == 'GET':
        try:
            application = IndustryProjectApplication.objects.get(pk=app_id)

            serializer = IndustryProjectApplicationSerializer(application, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        # end try-except
    # end if

    '''
    Partner accepts Member / Update Application
    '''
    if request.method == 'POST':
        try:
            application = IndustryProjectApplication.objects.get(pk=app_id)
            application.is_accepted = True
                        
            application.save() 

            serializer = IndustryProjectApplicationSerializer(application, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Delete an Application
    '''
    if request.method == 'DELETE':
        try:
            application = IndustryProjectApplication.objects.get(pk=app_id)
            application.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

@api_view(['DELETE'])
@permission_classes((IsMemberOrReadOnly,))
def delete_application_view(request, pk, app_id):

    '''
    Delete an Application
    '''
    if request.method == 'DELETE':
        try:
            application = IndustryProjectApplication.objects.get(pk=app_id)
            application.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

from .models import IndustryProject
from .serializers import IndustryProjectSerializer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from common.models import Partner
from common.permissions import IsPartnerOrReadOnly

@api_view(['GET', 'POST'])
@permission_classes((IsPartnerOrReadOnly,))
def industry_project_view(request):

    '''
    Get all Industry Projects
    '''
    if request.method == 'GET':
        try:
            industry_projects = IndustryProject.objects

            # extract query params
            search = request.query_params.get('search', None)
            is_available = request.query_params.get('isAvailable', None)
            is_completed = request.query_params.get('isCompleted', None)
            
            if search is not None:
                industry_projects = industry_projects.filter(
                    Q(title__icontains=search), 
                    Q(description__icontains=search) 
                )

            if is_available is not None:
                industry_projects = industry_projects.exclude(is_available=False)
            if is_completed is not None:
                industry_projects = industry_projects.exclude(is_completed=False)
            # end ifs

            serializer = IndustryProjectSerializer(industry_projects.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Create a new Industry Project
    '''
    if request.method == 'POST':
        try:
            data = request.data
            user = request.user
            partner = Partner.objects.get(user=user)

            industry_project = IndustryProject(
                title=data['title'],
                description=data['description'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                application_deadline=data['application_deadline'],        
                partner = partner,
            )
            industry_project.save()

            serializer = IndustryProjectSerializer(industry_project, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

from .models import IndustryProject
from .serializers import IndustryProjectSerializer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from common.models import Partner
from common.permissions import IsPartnerOrReadOnly

@api_view(['POST'])
@permission_classes((IsPartnerOrReadOnly,))
def industry_project_view(request):
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

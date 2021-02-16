from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Organization, Partner
from .serializers import OrganizationSerializer
from .permissions import IsPartnerOrAdminOrReadOnly


@api_view(['PUT'])
@permission_classes((IsPartnerOrAdminOrReadOnly,))
@parser_classes((MultiPartParser, FormParser))
def single_organization_view(request, pk):
    '''
    Updates organization details
    '''
    if request.method == 'PUT':
        try:
            user = request.user
            partner = Partner.objects.get(user=user)
            data = request.data

            organization = Organization.objects.filter(partners=partner).get(pk=pk)

            if 'organization_name' in data:
                organization.organization_name = data['organization_name']
            if 'organization_photo' in data:
                organization.organization_photo = data['organization_photo']
            # end ifs
            organization.save()

            return Response(OrganizationSerializer(organization, context={'request': request}).data, status=status.HTTP_200_OK)
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

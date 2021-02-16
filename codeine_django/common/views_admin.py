from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
)
from .models import BaseUser
from .serializers import NestedBaseUserSerializer


@api_view(['GET',])
@permission_classes((IsAdminUser,))
def admin_view(request):
    '''
    Get all Admin Users 
    '''
    if request.method == 'GET':
        # extract query params
        search = request.query_params.get('search', None)

        users = BaseUser.objects.exclude(is_admin=False)

        if search is not None:
            users = users.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        # end if

        serializer = NestedBaseUserSerializer(users.all(), many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def
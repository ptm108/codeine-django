from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import BaseUser
from common.serializers import NestedBaseUserSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def authenticate_user(request):
    '''
    Authenticate user credentials
    '''
    if request.method == 'POST':
        data = request.data
        user = authenticate(**data)

        if user is None:
            user = BaseUser.objects.filter(email=data['email']).first()

            # check user password
            if not user or not user.check_password(data['password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            return Response(NestedBaseUserSerializer(user, context={'request': request}).data, status=status.HTTP_403_FORBIDDEN)
        # end if

        # get JWT
        token = RefreshToken.for_user(user)

        payload = {
            'refresh': str(token),
            'access': str(token.access_token),
            'user': NestedBaseUserSerializer(user, context={'request': request}).data
        }

        return Response(payload, status=status.HTTP_200_OK)
    # end if
# end def

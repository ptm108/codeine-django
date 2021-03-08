from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)

import docker

@api_view(['GET'])
@permission_classes(['AllowAny'])
def init_ide(request):
    '''
    Test ide
    '''
    if request.method == 'GET':
        try:
            client = docker.from_env()
            client.containers.run('codercom/code-server')
        except:
            print('error')
        # end try except
    # end if
# end def

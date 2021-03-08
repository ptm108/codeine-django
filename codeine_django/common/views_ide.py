from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)

import docker
import os
import pwd


def get_username():
    return pwd.getpwuid(os.getuid())[0]
# end def


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def init_ide(request):
    '''
    Test ide
    '''
    if request.method == 'GET':
        user = request.user
        try:
            client = docker.from_env()
            container = client.containers.run(
                'code-server',
                detach=True,
                environment=[f'DOCKER_USER={get_username()}', 'GIT_URL=http://github.com/ptm108/photo-journal-rn'],
                user=f'{os.getuid()}:{os.getgid()}',
                name=f'code-server-{user.id}',
                ports={'8080/tcp': None},
            )
            container.reload()
            print(container.attrs)
            return Response()
        except Exception as e:
            print('error', e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # end try except
    # end if
# end def

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


@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated,))
def init_ide(request):
    user = request.user
    '''
    Init IDE and returns port number
    A user can only have 1 IDE active at any point in time
    '''
    if request.method == 'GET':
        client = docker.from_env()

        try:
            git_url = request.query_params.get('git_url', None)
            course_name = request.query_params.get('course_name', None)

            # if git_url is None:
            #     return Response('git_url is missing', status=status.HTTP_400_BAD_REQUEST)
            # end if

            container = client.containers.run(
                'codeine-ide',
                detach=True,
                environment=[f'GIT_URL={git_url}', f'COURSE_NAME={course_name.replace(" ", "-")}'],
                user='501:20',
                name=f'codeine-ide-{user.id}',
                ports={'8080/tcp': None},
            )
            container.reload()
            # print(container.attrs)

            return Response({'container_name': f'codeine-ide-{user.id}', 'port': container.attrs['NetworkSettings']['Ports']['8080/tcp'][0]['HostPort']}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            if str(e).split(' ')[0] == '409':
                # return Response(status=status.HTTP_409_CONFLICT)
                container = client.containers.get(f'codeine-ide-{user.id}')
                if container.attrs['State']['Status'] != 'running':
                    container.start()
                # end if
                container.reload()

                return Response({'container_name': f'codeine-ide-{user.id}', 'port': container.attrs['NetworkSettings']['Ports']['8080/tcp'][0]['HostPort']}, status=status.HTTP_200_OK)
            # end if
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # end try except
    # end if

    '''
    Stops and removes a container instance
    '''
    if request.method == 'DELETE':
        try:
            client = docker.from_env()
            container = client.containers.get(f'codeine-ide-{user.id}')
            container.stop()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def check_ide_status_view(request, port_number):
    user = request.user
    '''
    Returns true if IDE is ready, false otherwise
    '''
    if request.method == 'GET':
        client = docker.from_env()

        try:
            container = client.containers.get(f'codeine-ide-{user.id}')
            logs = container.logs()
            logs = logs.decode("utf-8").split('\n')
            curr = logs[-2].strip().split(' ')

            if len(curr) > 0 and curr[-1] == 'HTTPS':
                ready = True
            else:
                ready = False
            # end if else

            return Response({'logs': logs, 'ready': ready}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import (
    IsMemberOnly,
    IsMemberOrReadOnly
)
from .models import CV, Member
from .serializers import CVSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsMemberOrReadOnly,))
def cv_view(request):
    '''
    Get all CV by Member
    '''
    if request.method == 'GET':
        try:
            user = request.user
            member = Member.objects.get(user=user)

            cvs = CV.objects.filter(member=member)
            serializer = CVSerializer(
                cvs.all(), many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if

    '''
    Create a new CV
    '''
    if request.method == 'POST':
        try:
            data = request.data
            user = request.user
            member = Member.objects.get(user=user)

            cv = CV(
                title=data['title'],
                description=data['description'],
                organisation=data['organisation'],
                start_date=data['start_date'],
                end_date=data['end_date'],

                member=member
            )
            cv.save()

            serializer = CVSerializer(cv, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes((IsMemberOnly,))
def single_cv_view(request, pk):
    '''
    Get CV by ID
    '''
    if request.method == 'GET':
        try:
            cv = CV.objects.get(pk=pk)

            serializer = CVSerializer(cv, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Update CV
    '''
    if request.method == 'PATCH':
        try:
            data = request.data
            user = request.user
            cv = CV.objects.get(pk=pk)
            member = cv.member

            # assert that requesting member is the owner of the CV
            if member.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            if 'title' in data:
                cv.title = data['title']
            if 'description' in data:
                cv.description = data['description']
            if 'organisation' in data:
                cv.organisation = data['organisation']
            if 'start_date' in data:
                cv.start_date = data['start_date']
            if 'end_date' in data:
                cv.end_date = data['end_date']
            # end ifs

            cv.save()

            serializer = CVSerializer(cv, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, TypeError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Delete CV
    '''
    if request.method == 'DELETE':
        try:
            user = request.user
            cv = CV.objects.get(pk=pk)
            member = cv.member

            # assert that requesting member is the owner of the CV
            if member.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            cv.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def

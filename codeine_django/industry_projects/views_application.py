from .models import IndustryProject, IndustryProjectApplication
from .serializers import IndustryProjectApplicationSerializer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from common.models import Member
from common.permissions import IsPartnerOrReadOnly, IsMemberOrReadOnly
from datetime import date
from notifications.models import Notification, NotificationObject

@api_view(['GET'])
@permission_classes((IsMemberOrReadOnly,))
def member_application_view(request):
    '''
    Get all Member's Applications 
    '''
    if request.method == 'GET':
        try:
            user = request.user
            member = Member.objects.get(user=user)
            applications = IndustryProjectApplication.objects.filter(member=member)

            serializer = IndustryProjectApplicationSerializer(applications, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

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
            
            application = IndustryProjectApplication.objects.filter(member=member).filter(industry_project=industry_project).filter(is_rejected=False)

            if application.exists(): # already applied
                return Response("Member has already applied for this Industry Project", status=status.HTTP_409_CONFLICT)
            # end if

            today = date.today()
            if industry_project.application_deadline < today:  # application deadline has past
                return Response("The application deadline has past", status=status.HTTP_409_CONFLICT)
            # end if

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

@api_view(['GET', 'PATCH', 'DELETE'])
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
    Partner accepts/reject Member
    '''
    if request.method == 'PATCH':
        try:
            application = IndustryProjectApplication.objects.get(pk=app_id)

            data = request.data
            user = request.user
            industry_project = application.industry_project
            title = f''

            if 'is_accepted' in data:
                application.is_accepted = True
                title = f'Application for Industry Project {industry_project.title} accepted!'
                description = f'Partner {user} has accepted your application for Industry Project {industry_project.title}'
            if 'is_rejected' in data:
                application.is_rejected = True
                title = f'Application for Industry Project {industry_project.title} rejeceted!'
                description = f'Partner {user} has rejected your application for Industry Project {industry_project.title}'
            # end ifs
                                    
            application.save() 

            # notify member
            notification_type = 'CONSULTATION'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, industry_project=industry_project)
            notification.save()

            receiver = application.member.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()

            serializer = IndustryProjectApplicationSerializer(application, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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

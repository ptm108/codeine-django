from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from datetime import datetime

from .permissions import IsMemberOnly
from .models import MembershipSubscription, PaymentTransaction, Member
from .serializers import MembershipSubscriptionSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsMemberOnly,))
def membership_subscription_view(request):
    '''
    Creates a new payment transaction for a Membership Subscription
    '''
    if request.method == 'POST':
        data = request.data
        user = request.user
        member = Member.objects.get(user=user)

        with transaction.atomic():
            try:
                # check if there is a pending completion
                if MembershipSubscription.objects.filter(payment_transaction__payment_status='PENDING_COMPLETION'):
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                # end if

                month_duration = int(data['month_duration'])
                payment_transaction = PaymentTransaction(
                    payment_amount=(
                        float(data['subscription_fee']) * month_duration),
                    payment_type=data['payment_type']
                )
                payment_transaction.save()

                # get today's date or last contribution expiry date
                now = datetime.now()
                membership_subscription = MembershipSubscription.objects.filter(
                    Q(member=member)).first()

                if membership_subscription is not None:
                    now = membership_subscription.expiry_date
                    month_duration -= 1
                # end if

                year = now.year
                month = now.month + month_duration + 1  # first of the next month

                if month > 12:
                    month = month % 12 + 1
                    year += 1
                # end if

                expiry_date = timezone.make_aware(datetime(year, month, 1))

                membership_subscription = MembershipSubscription(
                    payment_transaction=payment_transaction,
                    member=member,
                    expiry_date=expiry_date,
                    month_duration=data['month_duration']
                )
                membership_subscription.save()

                serializer = MembershipSubscriptionSerializer(
                    membership_subscription, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValueError, KeyError) as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
    # end if

    '''
    Get Membership Subscription payments for the member
    '''
    if request.method == 'GET':
        user = request.user
        member = Member.objects.get(user=user)

        membership_subscriptions = MembershipSubscription.objects.filter(
            member=member)

        latest = request.query_params.get('latest', None)
        payment_status = request.query_params.get('payment_status', None)

        if payment_status is not None:
            membership_subscriptions = membership_subscriptions.filter(
                payment_transaction__payment_status=payment_status)
        if latest is not None:
            return Response(MembershipSubscriptionSerializer(membership_subscriptions.filter(expiry_date__gte=timezone.now()).order_by('expiry_date').first(), context={"request": request}).data, status=status.HTTP_200_OK)
        # end if

        serializer = MembershipSubscriptionSerializer(
            membership_subscriptions.all(), context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if
# end def


@api_view(['GET', 'DELETE'])
@permission_classes((IsMemberOnly,))
def single_membership_subscription_view(request, pk):
    '''
    Gets a Membership Subscription by primary key/ id
    '''
    if request.method == 'GET':
        try:
            membership_subscription = MembershipSubscription.objects.get(pk=pk)

            user = request.user
            member = membership_subscription.member

            # assert requesting member is getting their own Membership Subscription
            if member.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            serializer = MembershipSubscriptionSerializer(
                membership_subscription, context={"request": request})
            return Response(serializer.data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    '''
    Deletes a Membership Subscription by id
    '''
    if request.method == 'DELETE':
        try:
            membership_subscription = MembershipSubscription.objects.get(pk=pk)
            if membership_subscription.payment_transaction.payment_status != 'PENDING_COMPLETION':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end if
            user = request.user
            member = membership_subscription.member

            # assert requesting member is getting their own Membership Subscription
            if member.user != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

            membership_subscription.delete()
            return Response(MembershipSubscriptionSerializer(membership_subscription, context={"request": request}).data)
        except (ObjectDoesNotExist, KeyError, ValueError) as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if
# end def


@api_view(['PATCH'])
@permission_classes((IsMemberOnly,))
def update_membership_subscription_view(request, pk):
    '''
    Update Membership Subscription status
    '''
    if request.method == 'PATCH':
        data = request.data
        user = request.user
        member = Member.objects.get(user=user)
        membership_subscription = MembershipSubscription.objects.get(pk=pk)

        # assert requesting member is getting their own Membership Subscription
        if membership_subscription.member != member:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            # end if

        try:

            if 'payment_status' in data:
                membership_subscription.payment_transaction.payment_status = data['payment_status']
                if data['payment_status'] == 'COMPLETED':
                    member.membership_tier = 'PRO'
            # end if
            membership_subscription.payment_transaction.save()
            membership_subscription.save()
            member.save()

            serializer = MembershipSubscriptionSerializer(
                membership_subscription, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

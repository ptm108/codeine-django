from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Sum, Avg, Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)

from .models import EventLog
from common.models import MembershipSubscription, PaymentTransaction, BaseUser
from common.permissions import IsPartnerOnly
from courses.models import Enrollment

@api_view(['GET'])
@permission_classes((IsPartnerOnly,))
def earnings_report_view(request):
    '''
    Calculates the profits sans expenses, 
    and partner's cut of the profit pay out
    '''
    if request.method == 'GET':
        user = request.user
        try:
            partner = user.partner
            today = timezone.now()

            total_subscription_revenue = MembershipSubscription.objects.filter(expiry_date__gt=today).filter(payment_transaction__payment_status='COMPLETED').count() * 5.99
            total_subscription_revenue = total_subscription_revenue - BaseUser.objects.count() * 0.38 - 2700

            partner_enrollments = Enrollment.objects.filter(date_created__month=today.month).filter(course__partner=partner).count()
            total_enrollments = Enrollment.objects.filter(date_created__month=today.month).count()
            partner_cut = partner_enrollments / total_enrollments

            consultation_earnings = PaymentTransaction.objects.filter(
                Q(consultationpayment__consultation_application__consultation_slot__end_time__month=today.month) &
                Q(consultationpayment__consultation_application__consultation_slot__end_time__lte=today) &
                Q(payment_status='COMPLETED')
            ).aggregate(Sum('payment_amount'))
            print(consultation_earnings)

            pending_consultation_earnings = PaymentTransaction.objects.filter(
                Q(consultationpayment__consultation_application__consultation_slot__end_time__month=today.month) &
                Q(consultationpayment__consultation_application__consultation_slot__end_time__gt=today) &
                Q(payment_status='COMPLETED')
            ).aggregate(Sum('payment_amount'))
            print(pending_consultation_earnings)

            return Response({
                'month': today.month,
                'profit_sharing_pool': total_subscription_revenue,
                'partner_cut_percentage': partner_cut,
                'partner_cut_amount': partner_cut * total_subscription_revenue,
                'consultation_earnings': consultation_earnings['payment_amount__sum'],
                'pending_consultation_earnings': pending_consultation_earnings['payment_amount__sum']
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)
        # end try-except
    # end if
# end def

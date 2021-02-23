from rest_framework import serializers
from django.db.models import Q

from .models import ConsultationSlot, ConsultationPayment, ConsultationApplication
from common.serializers import NestedBaseUserSerializer, MemberSerializer, PaymentTransactionSerializer
from common.models import Member


class NestedConsultationApplicationSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_member_base_user')

    class Meta:
        model = ConsultationApplication
        fields = '__all__'
    # end Meta

    def get_member_base_user(self, obj):
        if obj.member is None:
            return None
        else:
            request = self.context.get("request")
            return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
        # end if-else
    # end def
# end class


class NestedConsultationSlotSerializer(serializers.ModelSerializer):
    number_of_signups = serializers.SerializerMethodField('get_number_of_signups')

    class Meta:
        model = ConsultationSlot
        fields = '__all__'
    # end Meta

    def get_number_of_signups(self, obj):
        confirmed_signups = ConsultationApplication.objects.filter(
            Q(consultation_slot=obj) &
            Q(is_cancelled=False) &
            Q(is_rejected=False)
        )
        return confirmed_signups.count()
    # end def
# end class


class ConsultationApplicationSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_member_base_user')
    consultation_slot = serializers.SerializerMethodField('get_consultation_slot')

    class Meta:
        model = ConsultationApplication
        fields = '__all__'
    # end Meta

    def get_member_base_user(self, obj):
        if obj.member is None:
            return None
        else:
            request = self.context.get("request")
            return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
        # end if-else
    # end def

    def get_consultation_slot(self, obj):
        consultation_slot = obj.consultation_slot
        return NestedConsultationSlotSerializer(consultation_slot).data
    # end def
# end class


class ConsultationSlotSerializer(serializers.ModelSerializer):
    # member = serializers.SerializerMethodField('get_member_base_user')
    partner = serializers.SerializerMethodField('get_partner_base_user')
    confirmed_applications = serializers.SerializerMethodField('get_confirmed_applications')

    class Meta:
        model = ConsultationSlot
        fields = '__all__'
    # end Meta

    def get_partner_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def

    def get_confirmed_applications(self, obj):
        consultation_applications = obj.consultation_applications.filter(
            Q(is_cancelled=False) &
            Q(is_rejected=False)
        )
        return NestedConsultationApplicationSerializer(consultation_applications, many=True).data
    # end def
# end class


class ConsultationPaymentSerializer(serializers.ModelSerializer):
    payment_transaction = PaymentTransactionSerializer()

    class Meta:
        model = ConsultationPayment
        fields = '__all__'
    # end Meta
# end class

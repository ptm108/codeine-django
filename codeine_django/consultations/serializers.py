from rest_framework import serializers
from django.db.models import Q

from .models import ConsultationSlot, ConsultationPayment, ConsultationApplication
from common.serializers import NestedBaseUserSerializer, MemberSerializer, NestedPaymentTransactionSerializer, MemberApplicationSerializer
from common.models import Member


class NestedConsultationApplicationSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    class Meta:
        model = ConsultationApplication
        fields = '__all__'
    # end Meta

    def get_member(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
    # end def
# end class


class NestedConsultationSlotSerializer(serializers.ModelSerializer):
    number_of_signups = serializers.SerializerMethodField(
        'get_number_of_signups')
    partner_name = serializers.SerializerMethodField('get_partner_name')

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

    def get_partner_name(self, obj):
        parter_name = obj.partner.user.first_name + ' ' + obj.partner.user.last_name
        return parter_name
    # end def
# end class


class NestedConsultationPaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField('get_member_name')

    class Meta:
        model = ConsultationPayment
        fields = '__all__'
    # end Meta

    def get_member_name(self, obj):
        member_name = obj.consultation_application.member.user.first_name + \
            ' ' + obj.consultation_application.member.user.last_name
        return member_name
    # end def
# end class


class ConsultationApplicationSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_member')
    consultation_slot = serializers.SerializerMethodField(
        'get_consultation_slot')
    consultation_payments = serializers.SerializerMethodField(
        'get_consultation_payments')

    class Meta:
        model = ConsultationApplication
        fields = '__all__'
    # end Meta

    def get_member(self, obj):
        request = self.context.get("request")
        return MemberApplicationSerializer(obj.member, context={'request': request}).data
        # end if-else
    # end def

    def get_consultation_slot(self, obj):
        request = self.context.get("request")
        consultation_slot = obj.consultation_slot
        return NestedConsultationSlotSerializer(consultation_slot).data
    # end def

    def get_consultation_payments(self, obj):
        request = self.context.get("request")
        consultation_payments = ConsultationPayment.objects.filter(
            consultation_application=obj)
        return NestedConsultationPaymentSerializer(consultation_payments, many=True).data
    # end def
# end class


class ConsultationSlotSerializer(serializers.ModelSerializer):
    # member = serializers.SerializerMethodField('get_member_base_user')
    partner = serializers.SerializerMethodField('get_partner_base_user')
    confirmed_applications = serializers.SerializerMethodField(
        'get_confirmed_applications')
    rejected_applications = serializers.SerializerMethodField(
        'get_rejected_applications')

    class Meta:
        model = ConsultationSlot
        fields = '__all__'
    # end Meta

    def get_partner_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def

    def get_confirmed_applications(self, obj):
        request = self.context.get("request")
        consultation_applications = obj.consultation_applications.filter(
            Q(is_cancelled=False) &
            Q(is_rejected=False)
        )
        return NestedConsultationApplicationSerializer(consultation_applications, context={'request': request}, many=True).data
    # end def

    def get_rejected_applications(self, obj):
        request = self.context.get("request")
        consultation_applications = obj.consultation_applications.filter(
            Q(is_rejected=True)
        )
        return NestedConsultationApplicationSerializer(consultation_applications, context={'request': request}, many=True).data
    # end def
# end class


class ConsultationPaymentSerializer(serializers.ModelSerializer):
    payment_transaction = NestedPaymentTransactionSerializer()
    consultation_slot = serializers.SerializerMethodField(
        'get_consultation_slot')
    member_name = serializers.SerializerMethodField('get_member_name')

    class Meta:
        model = ConsultationPayment
        fields = '__all__'
    # end Meta

    def get_consultation_slot(self, obj):
        request = self.context.get("request")
        consultation_slot = obj.consultation_application.consultation_slot
        return NestedConsultationSlotSerializer(consultation_slot, context={'request': request}).data
    # end def

    def get_member_name(self, obj):
        member_name = obj.consultation_application.member.user.first_name + \
            ' ' + obj.consultation_application.member.user.last_name
        return member_name
    # end def
# end class

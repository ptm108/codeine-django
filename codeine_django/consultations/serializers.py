from rest_framework import serializers

from .models import ConsultationSlot, PaymentTransaction, ConsultationPayment, ConsultationApplication
from common.serializers import NestedBaseUserSerializer

class ConsultationSlotSerializer(serializers.ModelSerializer):
    # member = serializers.SerializerMethodField('get_member_base_user')
    partner = serializers.SerializerMethodField('get_partner_base_user')

    class Meta:
        model = ConsultationSlot
        fields = '__all__'
    # end Meta

    # def get_member_base_user(self, obj):
    #     if obj.member is None:
    #         return None
    #     else:
    #         request = self.context.get("request")
    #         return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
    #     # end if-else
    # # end def

    def get_partner_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def
# end class

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
    # end Meta
# end class

class ConsultationPaymentSerializer(serializers.ModelSerializer):
    payment_transaction = PaymentTransactionSerializer()

    class Meta:
        model = ConsultationPayment
        fields = '__all__'
    # end Meta
# end class

class ConsultationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationApplication
        fields = '__all__'
    # end Meta
# end class

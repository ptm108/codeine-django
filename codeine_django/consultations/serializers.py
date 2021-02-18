from rest_framework import serializers

from .models import ConsultationSlot, PaymentTransaction


class ConsultationSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationSlot
        fields = '__all__'
    # end Meta
# end class

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
    # end Meta
# end class
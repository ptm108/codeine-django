from rest_framework import serializers

from .models import ConsultationSlot


class ConsultationSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationSlot
        fields = '__all__'
    # end Meta
# end class
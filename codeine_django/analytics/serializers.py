from rest_framework import serializers

from .models import EventLog
from common.serializers import NestedBaseUserSerializer


class EventLogSerializer(serializers.ModelSerializer):
    user = NestedBaseUserSerializer()

    class Meta:
        model = EventLog
        fields = '__all__'
    # end class

# end class

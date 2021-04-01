from rest_framework import serializers
from .models import Notification
from common.serializers import NestedBaseUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    receiver = NestedBaseUserSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
    # end Meta
# end class


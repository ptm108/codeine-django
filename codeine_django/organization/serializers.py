from rest_framework import serializers
from django.db.models import Q

from .models import ContributionPayment, Event, EventApplication, EventPayment
from common.serializers import PaymentTransactionSerializer, OrganizationSerializer, PartnerSerializer, NestedBaseUserSerializer
from common.models import Organization


class ContributionPaymentSerializer(serializers.ModelSerializer):
    payment_transaction = PaymentTransactionSerializer()
    organization = OrganizationSerializer()
    made_by = PartnerSerializer()

    class Meta:
        model = ContributionPayment
        fields = '__all__'
    # end Meta
# end class


class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Event
        fields = '__all__'
    # end Meta
# end class


class EventApplicationSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_member_base_user')
    event = EventSerializer()

    class Meta:
        model = EventApplication
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


class EventPaymentSerializer(serializers.ModelSerializer):
    payment_transaction = PaymentTransactionSerializer()

    class Meta:
        model = EventPayment
        fields = '__all__'
    # end Meta
# end class

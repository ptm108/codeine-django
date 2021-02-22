from rest_framework import serializers
from django.db.models import Q

from .models import ContributionPayment, Event, EventApplication
from common.serializers import PaymentTransactionSerializer, OrganizationSerializer, PartnerSerializer, NestedBaseUserSerializer
from common.models import Organization


class ContributionPaymentSerializer(serializers.ModelSerializer):
    payment_transaction = serializers.SerializerMethodField('get_payment_transaction')
    organization = serializers.SerializerMethodField('get_organization')
    made_by = serializers.SerializerMethodField('get_partner')

    class Meta:
        model = ContributionPayment
        fields = '__all__'
    # end Meta

    def get_payment_transaction(self, obj):
        payment_transaction = obj.payment_transaction
        return PaymentTransactionSerializer(payment_transaction).data
    # end def

    def get_organization(self, obj):
        organization = obj.organization
        return OrganizationSerializer(organization).data
    # end def

    def get_partner(self, obj):
        made_by = obj.made_by
        return PartnerSerializer(made_by).data
    # end def
# end class


class EventSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField('get_organization')

    class Meta:
        model = Event
        fields = '__all__'
    # end Meta

    def get_organization(self, obj):
        organization = obj.organization
        return OrganizationSerializer(organization).data
    # end def
# end class


class EventApplicationSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_member_base_user')
    event = serializers.SerializerMethodField('get_event')

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

    def get_event(self, obj):
        event = obj.event
        return EventSerializer(event).data
    # end def
# end class


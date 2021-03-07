from rest_framework import serializers

from .models import Ticket, TicketMessage


class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = '__all__'
    # end Meta
# end class


class TicketSerializer(serializers.ModelSerializer):
    ticket_messages = TicketMessageSerializer(many=True)

    class Meta:
        model = Ticket
        fields = '__all__'
    # end Meta
# end class

from rest_framework import serializers

from .models import Notification, NotificationObject
from common.models import PaymentTransaction
from common.serializers import NestedBaseUserSerializer, NestedMembershipSubscriptionSerializer
from courses.serializers import CourseSerializer
from community.serializers import ArticleSerializer, CodeReviewSerializer
from industry_projects.serializers import IndustryProjectSerializer
from consultations.serializers import ConsultationSlotSerializer, NestedConsultationPaymentSerializer
from organization.serializers import NestedEventPaymentSerializer, NestedContributionPaymentSerializer
from helpdesk.serializers import TicketSerializer


class PaymentTransactionSerializer(serializers.ModelSerializer):
    membership_subscription = serializers.SerializerMethodField('get_membership_subscription')
    event_payment = serializers.SerializerMethodField('get_event_payment')
    contribution_payment = serializers.SerializerMethodField('get_contribution_payment')
    consultation_payment = serializers.SerializerMethodField('get_consultation_payment')

    class Meta:
        model = PaymentTransaction
        fields = '__all__'
    # end Meta

    def get_membership_subscription(self, obj):
        request = self.context.get("request")
        try:
            if obj.membership_subscription:
                return NestedMembershipSubscriptionSerializer(obj.membership_subscription, context={'request': request}).data
            # end if
        except:
            print('membership subscription does not exist')
        # end try-except
    # end def

    def get_event_payment(self, obj):
        request = self.context.get("request")
        try:
            if obj.event_payment:
                return NestedEventPaymentSerializer(obj.event_payment, context={'request': request}).data
            # end if
        except:
            print('event payment does not exist')
        # end try-except
    # end def

    def get_contribution_payment(self, obj):
        request = self.context.get("request")
        try:
            if obj.contribution_payment:
                return NestedContributionPaymentSerializer(obj.contribution_payment, context={'request': request}).data
            # end if
        except:
            print('contribution payment does not exist')
        # end try-except
    # end def

    def get_consultation_payment(self, obj):
        request = self.context.get("request")
        try:
            if obj.consultation_payment:
                return NestedConsultationPaymentSerializer(obj.consultation_payment, context={'request': request}).data
            # end if
        except:
            print('consultation payment does not exist')
        # end try-except
    # end def 
# end class


class NestedNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    # end Meta
# end class


class NestedNotificationOjbectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationObject
        fields = '__all__'
    # end Meta
# end class


class NotificationSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('get_photo_url')
    sender = serializers.SerializerMethodField('get_sender')
    course = serializers.SerializerMethodField('get_course')
    article = serializers.SerializerMethodField('get_article')
    code_review = serializers.SerializerMethodField('get_code_review')
    transaction = serializers.SerializerMethodField('get_transaction')
    consultation_slot = serializers.SerializerMethodField(
        'get_consultation_slot')
    ticket = serializers.SerializerMethodField('get_ticket')
    industry_project = serializers.SerializerMethodField(
        'get_industry_project')
    transaction = serializers.SerializerMethodField('get_transaction')

    class Meta:
        model = Notification
        fields = '__all__'
    # end Meta

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        # end if
    # end def

    def get_sender(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.sender, context={'request': request}).data
    # end def

    def get_transaction(self, obj):
        request = self.context.get("request")
        if obj.transaction:
            return NestedPaymentTransactionSerializer(obj.transaction, context={'request': request}).data
        # end if
    # end def

    def get_course(self, obj):
        request = self.context.get("request")
        if obj.course:
            return CourseSerializer(obj.course, context={'request': request}).data
        # end if
    # end def

    def get_article(self, obj):
        request = self.context.get("request")
        if obj.article:
            return ArticleSerializer(obj.article, context={'request': request}).data
        # end if
    # end def

    def get_industry_project(self, obj):
        request = self.context.get("request")
        if obj.industry_project:
            return IndustryProjectSerializer(obj.industry_project, context={'request': request}).data
        # end if
    # end def

    def get_consultation_slot(self, obj):
        request = self.context.get("request")
        if obj.consultation_slot:
            return ConsultationSlotSerializer(obj.consultation_slot, context={'request': request}).data
        # end if
    # end def

    def get_code_review(self, obj):
        request = self.context.get("request")
        if obj.code_review:
            return CodeReviewSerializer(obj.code_review, context={'request': request}).data
        # end if
    # end def

    def get_ticket(self, obj):
        request = self.context.get("request")
        if obj.ticket:
            return TicketSerializer(obj.ticket, context={'request': request}).data
        # end if
    # end def

    def get_transaction(self, obj):
        request = self.context.get("request")
        if obj.transaction:
            return PaymentTransactionSerializer(obj.transaction, context={'request': request}).data
        # end if
    # end def
# end class


class NotificationObjectSerializer(serializers.ModelSerializer):
    receiver = serializers.SerializerMethodField('get_receiver')
    notification = serializers.SerializerMethodField('get_notification')
    num_unread = serializers.SerializerMethodField('get_num_unread')

    class Meta:
        model = NotificationObject
        fields = '__all__'
    # end Meta

    def get_receiver(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.receiver, context={'request': request}).data
    # end def

    def get_notification(self, obj):
        request = self.context.get("request")
        return NotificationSerializer(obj.notification, context={'request': request}).data
    # end def

    def get_num_unread(self, obj):
        receiver = obj.receiver
        num_unread = NotificationObject.objects.filter(receiver=receiver).filter(is_read=False).count()
        return num_unread
    # end def
# end class

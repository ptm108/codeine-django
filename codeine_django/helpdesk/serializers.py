from rest_framework import serializers

from .models import Ticket, TicketMessage
from common.serializers import NestedBaseUserSerializer, NestedPaymentTransactionSerializer
from courses.serializers import CourseSerializer
from community.serializers import ArticleSerializer, CodeReviewSerializer
from industry_projects.serializers import IndustryProjectSerializer
from consultations.serializers import ConsultationSlotSerializer


class NestedTicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = '__all__'
    # end Meta
# end class


class NestedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
    # end Meta
# end class


class TicketMessageSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField('get_file')
    base_user = serializers.SerializerMethodField('get_base_user')

    class Meta:
        model = TicketMessage
        fields = '__all__'
    # end Meta

    def get_file(self, obj):
        request = self.context.get("request")
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url)
        # end if
    # end def

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.base_user, context={'request': request}).data
    # end def
# end class


class TicketSerializer(serializers.ModelSerializer):
    ticket_messages = TicketMessageSerializer(many=True)

    photo = serializers.SerializerMethodField('get_photo_url')
    base_user = serializers.SerializerMethodField('get_base_user')
    transaction = serializers.SerializerMethodField('get_transaction')
    course = serializers.SerializerMethodField('get_course')
    article = serializers.SerializerMethodField('get_article')
    industry_project = serializers.SerializerMethodField(
        'get_industry_project')
    consultation_slot = serializers.SerializerMethodField(
        'get_consultation_slot')
    code_review = serializers.SerializerMethodField('get_code_review')

    class Meta:
        model = Ticket
        fields = '__all__'
    # end Meta

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url)
        # end if
    # end def

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.base_user, context={'request': request}).data
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
# end class


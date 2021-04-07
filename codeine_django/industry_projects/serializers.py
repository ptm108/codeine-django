from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from common.models import Member
from common.serializers import NestedBaseUserSerializer
from .models import (
    IndustryProject,
    IndustryProjectApplication
)


class IndustryProjectApplicationSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_base_user')

    class Meta:
        model = IndustryProjectApplication
        fields = '__all__'
    # end Meta

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
    # end def
# end class


class IndustryProjectSerializer(serializers.ModelSerializer):
    industry_project_applications = IndustryProjectApplicationSerializer(many=True)
    partner = serializers.SerializerMethodField('get_base_user')
    is_applied = serializers.SerializerMethodField('get_application')

    class Meta:
        model = IndustryProject
        fields = '__all__'
    # end Meta

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def

    def get_application(self, obj):
        request = self.context.get("request")
        user = request.user

        if (type(user) == AnonymousUser):
            return None
        # end if

        member = Member.objects.filter(user=user).first()
        # print(obj)

        if member is None:
            return member
        else:
            application = IndustryProjectApplication.objects.filter(member=member).filter(industry_project=obj)
            return application.exists()
        # end if-else
    # end def
# end class


class PartnerIndustryProjectSerializer(serializers.ModelSerializer):
    partner = serializers.SerializerMethodField('get_base_user')

    class Meta:
        model = IndustryProject
        fields = '__all__'
    # end Meta

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def
# end class


class NestedIndustryProjectApplicationSerializer(serializers.ModelSerializer):
    industry_project = PartnerIndustryProjectSerializer()

    class Meta:
        model = IndustryProjectApplication
        fields = '__all__'
    # end Meta
# end class

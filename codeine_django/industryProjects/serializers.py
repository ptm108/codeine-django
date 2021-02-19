from rest_framework import serializers
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
    class Meta:
        model = IndustryProject
        fields = '__all__'
    # end Meta

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def
# end class
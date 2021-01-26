from rest_framework import serializers

from .models import ContentProvider, Member, BaseUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('email', 'is_active', 'date_joined')
    # end Meta
# end class

class MemberSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Member
        fields = '__all__'
    # end Meta
# end class

class ContentProviderSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = ContentProvider
        fields = '__all__'
    # end Meta
# end class

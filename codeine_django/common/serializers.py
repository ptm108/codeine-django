from rest_framework import serializers

from .models import Member, BaseUser, IndustryPartner, ContentProvider, CodeineAdmin


class BaseUserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField('get_profile_photo_url')
    class Meta:
        model = BaseUser
        fields = ('email', 'is_active', 'date_joined', 'profile_photo', 'first_name', 'last_name')
    # end Meta

    def get_profile_photo_url(self, obj):
        request = self.context.get("request")
        if obj.profile_photo and hasattr(obj.profile_photo, 'url'):
            return request.build_absolute_uri(obj.profile_photo.url)
        # end if
    # end def
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

class IndustryPartnerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = IndustryPartner
        fields = '__all__'
    # end Meta
# end class

class CodeineAdminSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = CodeineAdmin
        fields = '__all__'
    # end Meta
# end class

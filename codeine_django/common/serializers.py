from rest_framework import serializers

from .models import Member, BaseUser, Partner, Organization, PaymentTransaction, BankDetail


class OrganizationSerializer(serializers.ModelSerializer):
    organization_photo = serializers.SerializerMethodField('get_organization_photo_url')

    def get_organization_photo_url(self, obj):
        request = self.context.get("request")
        if obj.organization_photo and hasattr(obj.organization_photo, 'url'):
            return request.build_absolute_uri(obj.organization_photo.url)
        # end if
    # end def

    class Meta:
        model = Organization
        fields = ('id', 'organization_name', 'organization_photo',)
    # end Meta
# end if


class NestedPartnerSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Partner
        fields = ('job_title', 'bio', 'organization')
        # fields = ('job_title', 'bio', 'consultation_rate', 'organization')
    # end Meta
# end class

class NestedMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id',)
    # end Meta
# end class


class NestedBaseUserSerializer(serializers.ModelSerializer):
    partner = NestedPartnerSerializer()
    member = NestedMemberSerializer()
    profile_photo = serializers.SerializerMethodField('get_profile_photo_url')

    class Meta:
        model = BaseUser
        fields = (
            'id',
            'email',
            'is_admin',
            'is_active',
            'date_joined',
            'profile_photo',
            'first_name',
            'last_name',
            'member',
            'partner',
        )
    # end Meta

    def get_profile_photo_url(self, obj):
        request = self.context.get("request")
        if obj.profile_photo and hasattr(obj.profile_photo, 'url'):
            return request.build_absolute_uri(obj.profile_photo.url)
        # end if
    # end def

# end class


class BaseUserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField('get_profile_photo_url')

    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'is_active', 'date_joined', 'profile_photo', 'first_name', 'last_name')
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


class PartnerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()
    
    class Meta:
        model = Member
        fields = '__all__'
    # end Meta
# end class


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
    # end Meta
# end class

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'
    # end Meta
# end class

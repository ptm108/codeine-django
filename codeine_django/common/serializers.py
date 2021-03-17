from rest_framework import serializers

from .models import Member, BaseUser, Partner, Organization, PaymentTransaction, BankDetail, MembershipSubscription, Notification, CV


class OrganizationSerializer(serializers.ModelSerializer):
    organization_photo = serializers.SerializerMethodField(
        'get_organization_photo_url')

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
        fields = ('id', 'stats', 'membership_tier')
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
            'is_suspended',
            'date_joined',
            'profile_photo',
            'first_name',
            'last_name',
            'age',
            'gender',
            'location',
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
        fields = ('id', 'email', 'is_active', 'date_joined',
                  'profile_photo', 'first_name', 'last_name', 'age', 'gender', 'location')
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
    partner = serializers.SerializerMethodField('get_base_user')

    class Meta:
        model = BankDetail
        fields = '__all__'
    # end Meta

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def
# end class


class MemberApplicationSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField('get_profile_photo_url')
    email = serializers.SerializerMethodField('get_email')
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')
    base_id = serializers.SerializerMethodField('get_base_user_id')

    class Meta:
        model = Member
        fields = ('id', 'base_id', 'email', 'profile_photo',
                  'first_name', 'last_name', 'membership_tier')
    # end Meta

    def get_profile_photo_url(self, obj):
        request = self.context.get("request")
        if obj.user.profile_photo and hasattr(obj.user.profile_photo, 'url'):
            return request.build_absolute_uri(obj.user.profile_photo.url)
        # end if
    # end def

    def get_email(self, obj):
        return obj.user.email
    # end def

    def get_first_name(self, obj):
        return obj.user.first_name
    # end def

    def get_last_name(self, obj):
        return obj.user.last_name
    # end def

    def get_base_user_id(self, obj):
        return obj.user.id
    # end def
# end class


class MembershipSubscriptionSerializer(serializers.ModelSerializer):
    payment_transaction = PaymentTransactionSerializer()
    member = MemberSerializer()

    class Meta:
        model = MembershipSubscription
        fields = '__all__'
    # end Meta
# end class


class NotificationSerializer(serializers.ModelSerializer):
    receiver = NestedBaseUserSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
    # end Meta
# end class


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = '__all__'
    # end Meta
# end class

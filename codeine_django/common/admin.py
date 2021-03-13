from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import BaseUser, Member, Partner, Organization, PaymentTransaction, MembershipSubscription, Notification


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = BaseUser
        fields = ('email',)
    # end class

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        # end if

        return password2

    # end def

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        # end if

        return user
    # end def
# end class


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = BaseUser
        fields = ('email', 'password', 'is_active', 'is_admin', 'first_name', 'last_name')
    # end class

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    # end def

# end class


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'Members'
# end class


class PartnerInline(admin.StackedInline):
    model = Partner
    can_delete = False
    verbose_name_plural = 'Partners'
# end class


class UserAdmin(BaseUserAdmin):
    # Vendor and Customer inline
    inlines = (MemberInline, PartnerInline,)

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'is_admin', 'is_active', 'is_suspended', 'profile_photo')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('id', 'email',)
    ordering = ('email',)
    filter_horizontal = ()

# end class


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
# end class


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
# end class


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization_name')
# end class


class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'payment_amount', 'payment_status', 'payment_type')
# end class


class MembershipSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_transaction', 'month_duration', 'expiry_date', 'member')
# end class


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'timestamp', 'is_read', 'get_receivers')

    def get_receivers(self, obj):
        return "\n".join([receiver.id for receiver in self.receivers.all()])
      
# end class


admin.site.register(BaseUser, UserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(MembershipSubscription, MembershipSubscriptionAdmin)
admin.site.register(Notification, NotificationAdmin)

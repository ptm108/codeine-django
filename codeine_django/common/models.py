from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import uuid


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)
# end def


def org_directory_path(instance, filename):
    return 'org_{0}/{1}'.format(instance.id, filename)
# end def


def get_default_member_stats():
    return {
        'PY': 0,
        'JAVA': 0,
        'JS': 0,
        'CPP': 0,
        'CS': 0,
        'HTML': 0,
        'CSS': 0,
        'RUBY': 0,
        'SEC': 0,
        'DB': 0,
        'FE': 0,
        'BE': 0,
        'UI': 0,
        'ML': 0,
    }
# end def


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    # end def

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        # end ifs

        return self.create_user(email, password, **extra_fields)
    # end def
# end class


class BaseUser(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown')
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    profile_photo = models.ImageField(
        upload_to=user_directory_path, max_length=100, blank=True, null=True, default=None)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    location = models.CharField(max_length=150, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}; {self.email}'
    # end def

    def has_perm(self, perm, obj=None):
        return super().has_perm(perm, obj=obj)
    # end def

    def has_module_perms(self, app_label):
        return super().has_module_perms(app_label)
    # end def

    @property
    def is_staff(self):
        return self.is_admin
    # end def

# end class


class Member(models.Model):
    MEMBERSHIP_TIERS = (
        ('FREE', 'Free'),
        ('PRO', 'Pro')
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=True)
    stats = models.JSONField(default=get_default_member_stats)

    # enums
    membership_tier = models.TextField(
        choices=MEMBERSHIP_TIERS, default='FREE')

    def __str__(self):
        return f'{self.user}'
    # end def
# end class


class Organization(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    organization_name = models.CharField(max_length=255, unique=True)
    organization_photo = models.ImageField(
        upload_to=org_directory_path, max_length=100, blank=True, null=True, default=None)

    def __str__(self):
        return self.organization_name
    # end def
# end class


class Partner(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, null=True, related_name='partner')
    job_title = models.CharField(
        max_length=150, null=True, default='', blank=True)
    bio = models.TextField(null=True, default='', blank=True)
    # consultation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    org_admin = models.BooleanField(default=False)

    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,
                                     related_name='partners', null=True, default=None, blank=True)

    def __str__(self):
        return f'{self.user}'
    # end def
# end class


class PaymentTransaction(models.Model):
    PAYMENT_STATUSES = (
        ('PENDING_COMPLETION', 'Pending Completion'),
        ('PENDING_REFUND', 'Pending Refund'),
        ('COMPLETED', 'Completed'),
        ('REFUNDED', 'Refunded'),
        ('FAILED', 'Failed')
    )

    PAYMENT_TYPES = (
        ('VISA', 'Visa'),
        ('MASTER', 'Mastercard'),
        ('AMEX', 'American Express')
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)

    # enums
    payment_status = models.TextField(
        choices=PAYMENT_STATUSES, default='PENDING_COMPLETION')
    payment_type = models.TextField(choices=PAYMENT_TYPES)

    def __str__(self):
        return f'Payment of {self.payment_amount} using {self.payment_type}, status: {self.payment_status}'
    # end def

    class Meta:
        ordering = ['timestamp']
    # end class
# end class


class BankDetail(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    bank_account = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    swift_code = models.CharField(max_length=20)
    bank_country = models.CharField(max_length=255)
    bank_address = models.CharField(max_length=255)

    partner = models.ForeignKey(
        'Partner', on_delete=models.CASCADE, related_name='bank_details')
# end class


class MembershipSubscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    payment_transaction = models.OneToOneField(
        PaymentTransaction, on_delete=models.CASCADE, related_name="membership_subscription")
    month_duration = models.PositiveSmallIntegerField(default=1)
    expiry_date = models.DateTimeField()

    # ref
    member = models.ForeignKey(
        Member, on_delete=models.SET_NULL, related_name='membership_subscriptions', null=True, blank=True)

    def __str__(self):
        return f'{self.payment_transaction} for {self.member}'
    # end def

    class Meta:
        ordering = ['expiry_date']
    # end Meta
# end class


class CV(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    organisation = models.CharField(max_length=100)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)

    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE, related_name='cvs')

    class Meta:
        ordering = ['-end_date', '-start_date']
    # end Meta
# end class

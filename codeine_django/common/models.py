from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import uuid


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
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        # end ifs 

        return self.create_user(email, password, **extra_fields)
    # end def
# end class


class BaseUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
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
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    # end def
# end class


class ContentProvider(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=150)
    bio = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    # end def
# end class


class IndustryPartner(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=11)

    def __str__(self):
        return self.company_name
    # end def
# end class

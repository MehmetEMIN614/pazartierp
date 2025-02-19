from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.utils.constants import UserRole
from apps.core.models.org import Org
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and extra fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure the superuser has these flags
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, null=True, blank=True, unique=True)
    role = models.IntegerField(default=UserRole.ACCOUNT_MANAGER, choices=UserRole.choices)
    phone_is_verified = models.BooleanField(default=False)
    mail_is_verified = models.BooleanField(default=False)
    orgs = models.ManyToManyField(Org, blank=True)
    current_org = models.ForeignKey(
        Org,
        on_delete=models.SET_NULL,
        null=True,
        related_name='current_users'
    )

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else ''

    def set_current_org(self, org):
        """Set current organization for user"""
        if org not in self.orgs.all():
            raise ValueError("User does not belong to this organization")
        self.current_org = org
        self.save(update_fields=['current_org'])

    def get_current_org(self):
        """Get current organization with fallback"""
        if self.current_org:
            return self.current_org
        # Fallback to first organization if no current org is set
        first_org = self.orgs.filter(active=True).first()
        if first_org:
            self.set_current_org(first_org)
            return first_org
        return None


class UserSetting(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    language = models.CharField(max_length=10, default='en-us')
    timezone = models.CharField(max_length=50, default='UTC')
    theme = models.CharField(max_length=20, default='light')
    notifications_enabled = models.BooleanField(default=True)

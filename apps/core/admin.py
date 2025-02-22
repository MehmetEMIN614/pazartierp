from django.apps import apps
from django.contrib import admin
from django.contrib.admin.exceptions import NotRegistered
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Enhanced admin view for custom User model"""
    list_display = [
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'phone_is_verified',
        'mail_is_verified'
    ]

    list_filter = [
        'is_active',
        'is_staff',
        'role',
        'phone_is_verified',
        'mail_is_verified',
        'groups'
    ]

    search_fields = [
        'email',
        'first_name',
        'last_name',
        'phone'
    ]

    # Customize fieldsets to include custom fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'phone',
                'role'
            )
        }),
        (_('Verification'), {
            'fields': (
                'phone_is_verified',
                'mail_is_verified'
            )
        }),
        (_('Organizations'), {
            'fields': (
                'orgs',
                'current_org'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined'
            )
        }),
    )

    # Customize add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'role',
                'phone'
            ),
        }),
    )

    # Ordering
    ordering = ['email']

    # Filter horizontal for many-to-many fields
    filter_horizontal = ('orgs',)


class CustomModelAdmin(admin.ModelAdmin):
    """Base ModelAdmin class for all models."""

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.list_filter = [
            field.name for field in model._meta.fields
            if isinstance(field, (models.BooleanField, models.DateField, models.DateTimeField))
               or field.name in ['status', 'type', 'category']
        ]
        self.search_fields = [
            field.name for field in model._meta.fields
            if isinstance(field, (models.CharField, models.TextField))
        ]
        # self.readonly_fields = ['created_at', 'updated_at']
        super().__init__(model, admin_site)


def auto_register_models():
    """Automatically register all models with Admin."""

    # Try to unregister Group if it's registered
    try:
        admin.site.unregister(Group)
    except NotRegistered:
        pass

    # Get all models
    app_models = apps.get_models()

    for model in app_models:
        try:
            # Skip models that are already registered or should be skipped
            if (model._meta.app_label in ['admin', 'sessions', 'contenttypes', 'auth'] or
                    model in [User, Group]):
                continue

            admin.site.register(model, CustomModelAdmin)

        except AlreadyRegistered:
            continue


# Call the registration function
auto_register_models()

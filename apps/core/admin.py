# apps/core/admin.py
from django.contrib import admin
from django.apps import apps
from django.contrib.admin.exceptions import NotRegistered
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom User model


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

    # Custom User admin
    @admin.register(User)
    class CustomUserAdmin(admin.ModelAdmin):
        list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']
        list_filter = ['is_active', 'is_staff', 'groups']
        search_fields = ['email', 'first_name', 'last_name']
        fieldsets = (
            ('Personal Info', {
                'fields': ('email', 'first_name', 'last_name', 'password')
            }),
            ('Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }),
            ('Important dates', {
                'fields': ('last_login', 'date_joined')
            }),
        )

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
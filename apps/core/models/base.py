from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Base model for all models in the system."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_created",
        verbose_name=_("Created by")
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_updated",
        verbose_name=_("Updated by")
    )
    active = models.BooleanField(default=True)
    org = models.ForeignKey(
        "core.Org",
        on_delete=models.CASCADE,
        verbose_name=_("Org"),
        related_name="%(class)s",
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Additional save logic if needed
        super().save(*args, **kwargs)


class BaseModelNoOrg(models.Model):
    """Base model for models that don't need Org field."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

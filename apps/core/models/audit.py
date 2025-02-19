from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class AuditLog(models.Model):
    """Audit log for tracking model changes."""
    action = models.CharField(max_length=20, choices=[
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ])

    # Which model was affected
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Who performed the action
    user = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )

    # When the action was performed
    timestamp = models.DateTimeField(auto_now_add=True)

    # Additional context
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=255, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)

    old_values = models.JSONField(null=True)
    new_values = models.JSONField(null=True)
    changes = models.JSONField(null=True)


    # Additional context
    app_label = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_str = models.CharField(max_length=255, null=True)

    # Organization context
    org = models.ForeignKey(
        "core.org",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"

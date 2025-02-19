from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from apps.core.models.audit import AuditLog


def create_audit_log(instance, action, old_values=None):
    """Helper function to create audit log"""
    AuditLog.objects.create(
        action=action,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=str(instance.pk),
        user=getattr(instance, 'updated_by', None),
        old_values=old_values,
        new_values=None if action == 'DELETE' else {
            field.name: str(getattr(instance, field.name))
            for field in instance._meta.fields
            if field.name not in ['created_at', 'updated_at']
        }
    )


@receiver(post_save)
def post_save_handler(sender, instance, created, **kwargs):
    """Handle all model saves"""
    # Skip certain models
    if sender._meta.model_name in ['auditlog', 'session', 'contenttype']:
        return

    action = 'CREATE' if created else 'UPDATE'
    create_audit_log(instance, action)


@receiver(pre_delete)
def pre_delete_handler(sender, instance, **kwargs):
    """Handle all model deletions"""
    # Skip certain models
    if sender._meta.model_name in ['auditlog', 'session', 'contenttype']:
        return

    create_audit_log(instance, 'DELETE')

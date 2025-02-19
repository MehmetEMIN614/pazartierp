from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, pre_delete


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    label = 'core'

    def ready(self):
        import apps.core.signals.audit

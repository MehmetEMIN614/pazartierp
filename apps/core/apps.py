from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    label = 'core'

    def ready(self):
        try:
            import apps.core.signals.audit
        except Exception as e:
            print(f"Error loading signals: {e}")

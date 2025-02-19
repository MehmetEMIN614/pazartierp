from apps.core.models.org import Org, OrgSetting
from django.db import transaction
from typing import Dict, Any


class OrgService:
    @staticmethod
    def create_org(name: str, address: str = None, note: str = None,
                   settings: Dict[str, Any] = None) -> Org:
        with transaction.atomic():
            org = Org.objects.create(
                name=name,
                address=address,
                note=note
            )

            # Create default settings
            default_settings = {
                'language': 'en-us',
                'timezone': 'UTC',
                'decimal_precision': 2
            }
            if settings:
                default_settings.update(settings)

            OrgSetting.objects.create(org=org, **default_settings)

            return org

    @staticmethod
    def update_org_settings(org: Org, settings: Dict[str, Any]) -> OrgSetting:
        org_settings = org.settings
        for key, value in settings.items():
            setattr(org_settings, key, value)
        org_settings.save()
        return org_settings
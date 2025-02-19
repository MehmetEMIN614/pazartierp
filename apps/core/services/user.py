from django.db import transaction
from django.core.exceptions import ValidationError
from apps.core.models.user import User, Org, UserSetting
from typing import List, Optional


class UserService:
    @staticmethod
    def create_user(email: str, password: str, first_name: str, last_name: str,
                    org: Optional[Org] = None, **extra_fields) -> User:
        with transaction.atomic():
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                **extra_fields
            )

            if org:
                user.orgs.add(org)
                user.current_org = org
                user.save()

            # Create default user settings
            UserSetting.objects.create(user=user, org=org)

            return user

    @staticmethod
    def assign_to_org(user: User, org: Org) -> None:
        if org in user.orgs.all():
            raise ValidationError("User already belongs to this organization")

        user.orgs.add(org)
        if not user.current_org:
            user.current_org = org
            user.save()

    @staticmethod
    def remove_from_org(user: User, org: Org) -> None:
        if org not in user.orgs.all():
            raise ValidationError("User does not belong to this organization")

        user.orgs.remove(org)
        if user.current_org == org:
            user.current_org = user.orgs.first()
            user.save()
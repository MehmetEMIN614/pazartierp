from django.db import models


class Currencies(models.IntegerChoices):
    USD = 1, "USD"
    TL = 2, "TL"


class UserRole(models.IntegerChoices):
    ADMIN = 1, "Admin"
    ACCOUNT_MANAGER = 2, "Account Manager"


class GenderTypes(models.IntegerChoices):
    ERKEK = 0
    KADIN = 1

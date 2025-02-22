from decimal import Decimal

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models.base import BaseModel


class Currencies(models.IntegerChoices):
    USD = 1, "USD"
    EUR = 2, "EUR"
    TRY = 3, "TRY"
    GBP = 4, "GBP"


class CurrencyRate(BaseModel):
    from_currency = models.IntegerField(choices=Currencies.choices)
    to_currency = models.IntegerField(choices=Currencies.choices)
    rate = models.DecimalField(decimal_places=6, max_digits=10)

    class Meta:
        unique_together = ['from_currency', 'to_currency']

    def clean(self):
        if self.from_currency == self.to_currency:
            raise ValidationError("From and To currencies cannot be the same")
        if self.rate <= 0:
            raise ValidationError("Rate must be greater than 0")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.clear_rate_cache()

    @classmethod
    def get_rate(cls, from_currency: int, to_currency: int) -> Decimal:
        if from_currency == to_currency:
            return Decimal('1.0')

        cache_key = f'currency_rate:{from_currency}:{to_currency}'
        rate = cache.get(cache_key)

        if rate is None:
            try:
                rate_obj = cls.objects.get(
                    from_currency=from_currency,
                    to_currency=to_currency
                )
                rate = rate_obj.rate
                cache.set(cache_key, rate, timeout=3600)  # Cache for 1 hour
            except cls.DoesNotExist:
                # Try reverse rate
                try:
                    rate_obj = cls.objects.get(
                        from_currency=to_currency,
                        to_currency=from_currency
                    )
                    rate = Decimal('1.0') / rate_obj.rate
                    cache.set(cache_key, rate, timeout=3600)
                except cls.DoesNotExist:
                    raise ValueError(f"No rate found for {from_currency} to {to_currency}")

        return rate

    def clear_rate_cache(self):
        """Clear cached rates for this currency pair."""
        cache_key = f'currency_rate:{self.from_currency}:{self.to_currency}'
        reverse_key = f'currency_rate:{self.to_currency}:{self.from_currency}'
        cache.delete_many([cache_key, reverse_key])

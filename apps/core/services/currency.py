from apps.core.models.currency import CurrencyRate
from decimal import Decimal
from typing import Dict, List
import requests


class CurrencyService:
    @staticmethod
    def update_rate(from_currency: int, to_currency: int,
                    rate: Decimal) -> CurrencyRate:
        currency_rate, created = CurrencyRate.objects.get_or_create(
            from_currency=from_currency,
            to_currency=to_currency,
            defaults={'rate': rate}
        )

        if not created:
            currency_rate.rate = rate
            currency_rate.save()

        return currency_rate

    @staticmethod
    def get_conversion_rate(from_currency: int, to_currency: int) -> Decimal:
        return CurrencyRate.get_rate(from_currency, to_currency)

    @staticmethod
    def convert_amount(amount: Decimal, from_currency: int,
                       to_currency: int) -> Decimal:
        if from_currency == to_currency:
            return amount

        rate = CurrencyRate.get_rate(from_currency, to_currency)
        return amount * rate

    @classmethod
    def update_rates_from_api(cls, api_key: str) -> List[CurrencyRate]:
        """
        Update currency rates from external API
        Example using exchangerate-api.com
        """
        base_url = "https://v6.exchangerate-api.com/v6"
        currencies = [choice[0] for choice in CurrencyRate.Currencies.choices]
        updated_rates = []

        for from_currency in currencies:
            response = requests.get(f"{base_url}/{api_key}/latest/{from_currency}")
            if response.status_code == 200:
                rates = response.json().get('conversion_rates', {})
                for to_currency in currencies:
                    if from_currency != to_currency:
                        rate = Decimal(str(rates.get(to_currency, 0)))
                        if rate > 0:
                            updated_rates.append(
                                cls.update_rate(from_currency, to_currency, rate)
                            )

        return updated_rates

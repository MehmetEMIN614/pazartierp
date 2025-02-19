from rest_framework import status

from apps.core.models.currency import CurrencyRate
from apps.core.views.base import BaseModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


class CurrencyRateViewSet(BaseModelViewSet):
    queryset = CurrencyRate.objects.all()
    filterset_fields = ['from_currency', 'to_currency']
    ordering_fields = ['rate', 'created_at']

    @action(detail=False, methods=['get'])
    def convert(self, request):
        """Currency conversion endpoint"""
        from_curr = request.query_params.get('from')
        to_curr = request.query_params.get('to')
        amount = request.query_params.get('amount')

        try:
            rate = CurrencyRate.get_rate(int(from_curr), int(to_curr))
            converted = float(amount) * float(rate)
            return Response({
                'from': from_curr,
                'to': to_curr,
                'rate': rate,
                'amount': amount,
                'converted': converted
            })
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )

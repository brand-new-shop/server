from rest_framework import serializers


class CoinbasePaymentCreateSerializer(serializers.Serializer):
    payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

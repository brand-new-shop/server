from decimal import Decimal

import coinbase_commerce
from django.conf import settings
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from payments.models import CoinbasePayment
from payments.services import create_charge


class CoinbasePaymentCreateAPI(APIView):
    class InputSerializer(serializers.Serializer):
        payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def post(self, request: Request, telegram_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_amount: Decimal = serializer.data['payment_amount']
        user = get_object_or_404(User, telegram_id=telegram_id)
        client = coinbase_commerce.Client(settings.COINBASE_API_KEY)
        charge = create_charge(client, telegram_id, payment_amount)
        CoinbasePayment.objects.create(user=user, uuid=charge.uuid, payment_amount=payment_amount)
        return Response({'uuid': charge.uuid, 'hosted_url': charge.hosted_url}, status=status.HTTP_201_CREATED)

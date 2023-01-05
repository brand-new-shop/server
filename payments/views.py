import coinbase_commerce
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from accounts.models import User
from payments.serializers import CoinbasePaymentCreateSerializer
from payments.models import CoinbasePayment


@api_view(['POST'])
def coinbase_payment_create_view(request, telegram_id: int):
    serializer = CoinbasePaymentCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(User, telegram_id=telegram_id)

    serialized_data = serializer.data
    payload = {
        "name": 'Balance top-up',
        "description": None,
        "local_price": {
            "amount": serialized_data['payment_amount'],
            "currency": "USD"
        },
        "pricing_type": "fixed_price"
    }
    client = coinbase_commerce.Client(settings.COINBASE_API_KEY)
    charge = client.charge.create(**payload)
    CoinbasePayment.objects.create(user=user, uuid=charge['id'], payment_amount=serialized_data['payment_amount'])
    response_data = {'uuid': charge['id'], 'hosted_url': charge['hosted_url']}
    return Response(response_data)

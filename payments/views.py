import coinbase_commerce
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from accounts.models import User
from payments.models import CoinbasePayment
from payments.serializers import CoinbasePaymentCreateSerializer
from payments.services import create_charge


@api_view(['POST'])
def coinbase_payment_create_view(request, telegram_id: int):
    serializer = CoinbasePaymentCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    payment_amount = serializer.data['payment_amount']

    user = get_object_or_404(User, telegram_id=telegram_id)
    client = coinbase_commerce.Client(settings.COINBASE_API_KEY)
    charge = create_charge(client, telegram_id, payment_amount)
    CoinbasePayment.objects.create(user=user, uuid=charge.uuid, payment_amount=payment_amount)

    response_data = {'uuid': charge.uuid, 'hosted_url': charge.hosted_url}
    return Response(response_data)

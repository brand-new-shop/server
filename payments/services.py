import logging
from decimal import Decimal
from uuid import UUID

import coinbase_commerce
from coinbase_commerce.error import ResourceNotFoundError
from django.db import transaction

from accounts.models import User
from payments.models import CoinbasePayment
from payments.schemas import CoinbaseCharge
from payments.exceptions import CoinbasePaymentNotFoundError


def create_charge(
        client: coinbase_commerce.Client,
        telegram_id: int,
        payment_amount: Decimal,
) -> CoinbaseCharge:
    charge = client.charge.create(
        name=f'User {telegram_id} balance top-up',
        description=None,
        local_price={'amount': payment_amount, 'currency': 'USD'},
        pricing_type='fixed_price',
    )
    return CoinbaseCharge(
        uuid=UUID(charge['id']),
        payment_amount=payment_amount,
        hosted_url=charge['hosted_url'],
        status=charge['timeline'][-1]['status'],
        context=charge['timeline'][-1].get('context'),
    )


def get_charge(client: coinbase_commerce.Client, charge_uuid: UUID) -> CoinbaseCharge:
    try:
        charge = client.charge.retrieve(str(charge_uuid))
    except ResourceNotFoundError:
        raise CoinbasePaymentNotFoundError(payment_uuid=charge_uuid)
    return CoinbaseCharge(
        uuid=charge['id'],
        payment_amount=Decimal(charge['pricing']['local']['amount']),
        hosted_url=charge['hosted_url'],
        status=charge['timeline'][-1]['status'],
        context=charge['timeline'][-1].get('context'),
    )


@transaction.atomic
def top_up_user_balance(user: User, coinbase_payment: CoinbasePayment):
    user.balance = user.balance + coinbase_payment.payment_amount
    user.save()
    logging.info('User balance has been refilled')
    coinbase_payment.delete()
    logging.info(f'Coinbase payment {str(coinbase_payment.uuid)} was deleted')

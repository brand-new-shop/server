import logging

import coinbase_commerce
from celery import shared_task
from django.conf import settings
from django.db import transaction, DatabaseError

from payments.models import CoinbasePayment
from payments.services import get_charge, top_up_user_balance


@shared_task
def coinbase_user_payments_sync():
    client = coinbase_commerce.Client(settings.COINBASE_API_KEY)
    coinbase_payments = CoinbasePayment.objects.select_related('user').all()
    for coinbase_payment in coinbase_payments:
        charge = get_charge(client, coinbase_payment.uuid)
        logging.debug(charge)
        if charge.status not in ('EXPIRED', 'CANCELED', 'UNRESOLVED', 'COMPLETED') or charge.context != 'OVERPAID':
            continue
        logging.info(f'New paid charge {charge}')
        top_up_user_balance(coinbase_payment.user, coinbase_payment)

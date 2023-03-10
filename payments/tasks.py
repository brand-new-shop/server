import logging

import coinbase_commerce
from celery import shared_task
from django.conf import settings

from accounts.tasks import send_balance_refilled_notification_to_user
from payments.models import CoinbasePayment
from payments.services import get_charge, top_up_user_balance
from payments.exceptions import CoinbasePaymentNotFoundError


@shared_task
def coinbase_user_payments_sync():
    client = coinbase_commerce.Client(settings.COINBASE_API_KEY)
    coinbase_payments = CoinbasePayment.objects.select_related('user').all()
    for coinbase_payment in coinbase_payments:
        try:
            charge = get_charge(client, coinbase_payment.uuid)
        except CoinbasePaymentNotFoundError:
            coinbase_payment.delete()
            logging.warning(f'Coinbase payment {str(coinbase_payment.uuid)} was not found on the provider side and was deleted')
            continue
        logging.debug(charge)
        if charge.status not in ('EXPIRED', 'CANCELED', 'UNRESOLVED', 'COMPLETED') or charge.context != 'OVERPAID':
            continue
        logging.info(f'New paid charge {charge}')
        user = coinbase_payment.user
        top_up_user_balance(user, coinbase_payment)
        send_balance_refilled_notification_to_user.delay(user.telegram_id, coinbase_payment.payment_amount)

from django.db.models import QuerySet

from payments.models import CoinbasePayment


def get_pending_coinbase_payments() -> QuerySet[CoinbasePayment]:
    return (
        CoinbasePayment.objects
        .select_related('user')
        .filter(type=CoinbasePayment.Status.PENDING)
    )

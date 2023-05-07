from django.urls import path
from payments.views import (
    BalanceTopUpViaCoinbasePaymentCreateApi,
    PaymentForOrderViaCoinbaseCreateApi,
)

urlpatterns = [
    path(
        'users/telegram-id/<int:telegram_id>/payments/coinbase/',
        BalanceTopUpViaCoinbasePaymentCreateApi.as_view(),
    ),
    path(
        'users/telegram-id/<int:telegram_id>/payments/coinbase/cart/',
        PaymentForOrderViaCoinbaseCreateApi.as_view(),
    ),
]

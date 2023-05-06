from django.urls import path
from payments.views import BalanceTopUpViaCoinbasePaymentCreateApi

urlpatterns = [
    path(
        'users/telegram-id/<int:telegram_id>/payments/coinbase/',
        BalanceTopUpViaCoinbasePaymentCreateApi.as_view(),
    ),
]

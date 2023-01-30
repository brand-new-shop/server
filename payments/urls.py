from django.urls import path
from payments.views import CoinbasePaymentCreateAPI

urlpatterns = [
    path('users/telegram-id/<int:telegram_id>/payments/coinbase/', CoinbasePaymentCreateAPI.as_view()),
]

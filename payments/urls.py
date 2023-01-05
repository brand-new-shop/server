from django.urls import path
from payments.views import coinbase_payment_create_view

urlpatterns = [
    path('users/telegram-id/<int:telegram_id>/payments/coinbase/', coinbase_payment_create_view),
]

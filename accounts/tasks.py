from decimal import Decimal

from celery import shared_task
from django.conf import settings

from accounts.telegram import TelegramBot


@shared_task
def send_balance_refilled_notification_to_user(telegram_id: int, payment_amount: Decimal) -> None:
    text = f'✅ Balance was topped up by {payment_amount}$'
    telegram_bot = TelegramBot(settings.TELEGRAM_BOT_TOKEN)
    telegram_bot.send_message(telegram_id, text)

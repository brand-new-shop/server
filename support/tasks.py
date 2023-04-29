import textwrap

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from support.models import SupportTicket
from telegram.services import TelegramBot


@shared_task
def ticket_status_changed(telegram_id: int, ticket_id: int):
    ticket = SupportTicket.objects.get(id=ticket_id)
    now = timezone.now()
    telegram_bot = TelegramBot(settings.TELEGRAM_BOT_TOKEN)
    template = textwrap.dedent(f'''\
    Ticket Update:
    Date: {now:%m/%d/%Y %H:%M}
    Ticket Number: #{ticket.id}
    Current Ticket Status: {ticket.Status(ticket.status).label}
    Message: {ticket.answer}''')

    match ticket.status:
        case SupportTicket.Status.ON_HOLD:
            template += (
                '\nFor the On-Hold statuses,'
                ' please expect longer waiting times.'
                ' Rest assured that our team is working on your case'
            )
        case SupportTicket.Status.PENDING:
            template += (
                '\nOur team is following up your ticket.'
                ' We will respond in few hours'
            )
    telegram_bot.send_message(chat_id=telegram_id, text=template)

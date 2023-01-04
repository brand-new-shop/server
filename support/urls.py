from django.urls import path

from support.views import (
    SupportTicketListCreateView,
    SupportTicketRetrieveUpdateView,
    ReplyToTicketListCreateView,
    ReplyToTicketRetrieveView,
)

urlpatterns = [
    path('users/telegram-id/<int:telegram_id>/tickets/', SupportTicketListCreateView.as_view()),
    path('tickets/<int:ticket_id>/', SupportTicketRetrieveUpdateView.as_view()),
    path('tickets/<int:ticket_id>/replies/', ReplyToTicketListCreateView.as_view()),
    path('tickets/replies/<int:reply_id>/', ReplyToTicketRetrieveView.as_view()),
]

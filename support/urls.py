from django.urls import path

from support.views import SupportTicketListCreateView, SupportTicketRetrieveView

urlpatterns = [
    path('users/telegram-id/<int:telegram_id>/tickets/', SupportTicketListCreateView.as_view()),
    path('tickets/<int:ticket_id>/', SupportTicketRetrieveView.as_view()),
]

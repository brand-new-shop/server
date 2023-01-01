from django.urls import path

from accounts.views import user_create_view, UserDetailView, OrdersListCreateView, orders_count_view
from support.views import SupportTicketListCreateView, SupportTicketRetrieveView

urlpatterns = [
    path('', user_create_view),
    path('telegram-id/<int:telegram_id>/', UserDetailView.as_view()),
    path('telegram-id/<int:telegram_id>/orders/', OrdersListCreateView.as_view()),
    path('telegram-id/<int:telegram_id>/orders/statistics/', orders_count_view),
    path('telegram-id/<int:telegram_id>/tickets/', SupportTicketListCreateView.as_view()),
    path('telegram-id/<int:telegram_id>/tickets/<int:ticket_id>/', SupportTicketRetrieveView.as_view()),
]

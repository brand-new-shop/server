from django.urls import path

from accounts.views import user_create_view, UserDetailView, OrdersListCreateView, orders_count_view

urlpatterns = [
    path('', user_create_view),
    path('telegram-id/<int:telegram_id>/', UserDetailView.as_view()),
    path('telegram-id/<int:telegram_id>/orders/', OrdersListCreateView.as_view()),
    path('telegram-id/<int:telegram_id>/orders/statistics/', orders_count_view),
]

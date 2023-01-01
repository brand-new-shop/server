from django.urls import path

from support.views import (
    SupportRequestListCreateView,
    SupportRequestRetrieveView,
)

urlpatterns = [
    path('requests/<int:support_request_id>/', SupportRequestRetrieveView.as_view()),
    path('requests/users/telegram-id/<int:user_telegram_id>/', SupportRequestListCreateView.as_view()),
]

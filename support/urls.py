from django.urls import path

from support.views import (
    SupportSubjectsListCreateView,
    SupportSubjectsRetrieveView,
    SupportRequestListCreateView,
    SupportRequestRetrieveView,
)

urlpatterns = [
    path('', SupportSubjectsListCreateView.as_view()),
    path('<int:support_subject_id>/', SupportSubjectsRetrieveView.as_view()),
    path('requests/<int:support_request_id>/', SupportRequestRetrieveView.as_view()),
    path('requests/users/telegram-id/<int:user_telegram_id>/', SupportRequestListCreateView.as_view()),
]

from django.urls import path

from accounts.views import (
    UserCreateApi,
    UserRetrieveUpdateApi,
)

urlpatterns = [
    path('', UserCreateApi.as_view()),
    path('telegram-id/<int:telegram_id>/', UserRetrieveUpdateApi.as_view()),
]

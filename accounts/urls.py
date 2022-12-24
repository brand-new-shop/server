from django.urls import path

from accounts.views import user_create_view, UserDetailView

urlpatterns = [
    path('', user_create_view),
    path('telegram-id/<int:telegram_id>/', UserDetailView.as_view()),
]

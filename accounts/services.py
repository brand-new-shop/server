from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import APIException

from accounts.models import User
from accounts.exceptions import UserNotFound

__all__ = ('get_user_or_raise_404',)


def get_user_or_raise_404(telegram_id: int) -> User:
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        raise UserNotFound


def create_user(telegram_id: int, username: str | None = None) -> User:
    return User.objects.create(telegram_id=telegram_id, username=username)


def update_username(telegram_id: int, username: str | None = None) -> bool:
    return bool(
        User.objects
        .filter(telegram_id=telegram_id)
        .update(username=username)
    )

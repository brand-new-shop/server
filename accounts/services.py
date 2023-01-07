from accounts.models import User
from accounts.exceptions import UserNotFound

__all__ = ('get_user_or_raise_404',)


def get_user_or_raise_404(telegram_id: int) -> User:
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        raise UserNotFound

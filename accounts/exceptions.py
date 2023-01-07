from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class UserNotFound(NotFound):
    default_detail = _('User is not found')

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class ProductNotFound(NotFound):
    default_detail = _('Product is not found')

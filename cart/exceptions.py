from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import NotFound, APIException, PermissionDenied


class NotEnoughProductStocks(NotFound):
    default_detail = _('Not enough product stocks')


class ProductAlreadyExistsInCart(APIException):
    default_detail = _('Product is already exists in cart')
    status_code = status.HTTP_409_CONFLICT


class CartProductNotFound(NotFound):
    default_detail = _('Cart product is not found')

from uuid import UUID

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class CoinbasePaymentNotFoundError(Exception):
    def __init__(self, *, payment_uuid: UUID):
        super().__init__(f'Payment by ID {str(payment_uuid)} is not found')
        self.payment_uuid = payment_uuid


class ZeroAmountChargeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The Coinbase payment charge has a zero amount.")
    default_code = "zero_amount_charge"

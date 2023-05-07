from django.db import models

from accounts.models import User


class CoinbasePayment(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1
        SUCCESS = 2
        FAILED = 3

    class Type(models.IntegerChoices):
        BALANCE_TOP_UP = 1
        PAYMENT_FOR_ORDER = 2

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.PENDING,
    )
    type = models.PositiveSmallIntegerField(choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Coinbase: {str(self.uuid)}'

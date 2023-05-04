from django.db import models

from accounts.models import User


class CoinbasePayment(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1
        SUCCESS = 2
        FAILED = 3

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return f'Coinbase: {str(self.uuid)}'

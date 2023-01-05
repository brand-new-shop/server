from django.db import models

from accounts.models import User


class CoinbasePayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Coinbase: {str(self.uuid)}'

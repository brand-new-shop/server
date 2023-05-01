from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import User
from products.models import Product


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=(MinValueValidator(1),))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(
        validators=(MinValueValidator(1),)
    )
    product_price_at_the_moment = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total_price(self) -> Decimal:
        return self.product_price_at_the_moment * self.quantity

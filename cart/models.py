from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import User
from products.models import Product


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=(MinValueValidator(1),))

    class Meta:
        unique_together = ('user', 'product')

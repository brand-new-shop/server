from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import User


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    emoji_icon = models.CharField(max_length=64, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(
        help_text='the bigger number the higher priority')
    parent = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,
                               blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('parent', 'priority')

    def __str__(self):
        if self.emoji_icon is not None:
            return f'{self.emoji_icon} {self.name}'
        return self.name

    def clean(self):
        if self.parent == self:
            raise ValidationError(
                'Parent category cannot be the same as current category.'
            )
        return super().clean()


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stocks_count = models.PositiveSmallIntegerField(default=0)
    min_order_quantity = models.PositiveSmallIntegerField(default=1)
    max_order_quantity = models.PositiveSmallIntegerField(default=1)
    max_replacement_time_in_minutes = models.PositiveIntegerField(default=15)
    are_stocks_displayed = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
    can_be_purchased = models.BooleanField(default=True)
    is_balance_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f'#{self.id}'


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

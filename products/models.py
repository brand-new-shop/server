from django.db import models

from accounts.models import User


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    emoji_icon = models.CharField(max_length=8, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    parent = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        if self.emoji_icon is not None:
            return f'{self.emoji_icon} {self.name}'
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture_url = models.ImageField(null=True, blank=True, upload_to='pictures')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stocks_count = models.SmallIntegerField(default=0)
    content = models.TextField()
    type = models.CharField(max_length=64, default='text')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.SmallIntegerField()
    payment_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} | {self.product}'

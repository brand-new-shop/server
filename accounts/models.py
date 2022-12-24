from django.db import models


class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        name = f'User {self.telegram_id}'
        if self.username is not None:
            name += f' | @{self.username}'
        return name

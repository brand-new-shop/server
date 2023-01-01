from django.db import models


class ShopInfo(models.Model):
    KEYS = (
        ('faq', 'FAQ'),
        ('rules', 'Rules'),
    )
    key = models.CharField(max_length=255, choices=KEYS, unique=True)
    value = models.TextField()

    class Meta:
        verbose_name_plural = 'shop info'

    def __str__(self):
        return self.get_key_display()

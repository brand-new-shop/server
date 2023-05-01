from django.contrib import admin

from cart.models import CartProduct, Order


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    search_fields = ('id', 'user__telegram_id')
    search_help_text = 'Search by order ID or user Telegram ID'

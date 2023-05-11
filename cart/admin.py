from django.contrib import admin

from cart.models import CartProduct, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    can_delete = False
    extra = 0


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    search_fields = ('id', 'user__telegram_id')
    search_help_text = 'Search by order ID or user Telegram ID'
    inlines = (OrderProductInline,)


@admin.register(OrderProduct)
class OrderProduct(admin.ModelAdmin):

    readonly_fields = ('total_cost',)

    @admin.display
    def total_cost(self, obj: OrderProduct):
        return obj.product_price_at_the_moment * obj.quantity

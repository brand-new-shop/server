from django.contrib import admin

from payments.models import CoinbasePayment


@admin.register(CoinbasePayment)
class CoinbasePaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at',)
    list_filter = ('status', 'type')
    readonly_fields = ('created_at',)

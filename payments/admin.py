from django.contrib import admin

from payments.models import CoinbasePayment


@admin.register(CoinbasePayment)
class CoinbasePaymentAdmin(admin.ModelAdmin):
    pass

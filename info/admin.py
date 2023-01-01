from django.contrib import admin

from info.models import ShopInfo


@admin.register(ShopInfo)
class ShopInfoAdmin(admin.ModelAdmin):
    pass

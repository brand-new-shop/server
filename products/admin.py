from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from products.models import Category, Product, Order


class CategoryParentListFilter(SimpleListFilter):
    title = _('category_without_parent')
    parameter_name = 'category_without_parent'

    def lookups(self, request, model_admin):
        return (
            ('categories', _('Categories')),
            ('subcategories', _('Subcategories')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'categories':
            return queryset.filter(parent=None)
        elif self.value() == 'subcategories':
            return queryset.exclude(parent=None)
        return queryset


class CategoryInline(admin.TabularInline):
    model = Category
    verbose_name = 'subcategory'
    verbose_name_plural = 'subcategories'


class ProductInline(admin.StackedInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = (CategoryParentListFilter,)
    inlines = (CategoryInline, ProductInline)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    search_fields = ('id', 'user__telegram_id')
    search_help_text = 'Search by order ID or user Telegram ID'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_select_related = ('category',)
    list_filter = ('category',)
    ordering = ('name',)
    search_fields = ('name',)
    search_help_text = 'Search by product\'s name'

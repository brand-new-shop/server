from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from products.models import Category, Product, ProductPicture


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
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProductInline(admin.StackedInline):
    model = Product


class ProductPictureInline(admin.StackedInline):
    model = ProductPicture
    classes = ('collapse',)
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = (CategoryParentListFilter,)
    ordering = ('priority',)
    list_display = ('__str__', 'priority',)
    inlines = (CategoryInline,)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_select_related = ('category',)
    list_filter = ('category',)
    ordering = ('name',)
    search_fields = ('name',)
    search_help_text = 'Search by product\'s name'
    inlines = (ProductPictureInline,)
    autocomplete_fields = ('category',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'category',
                'price',
                'stocks_count',
            )
        }),
        ('Specific Advanced Settings', {
            'classes': ('collapse',),
            'fields': (
                (
                    'min_order_quantity',
                    'max_order_quantity',
                ),
                'max_replacement_time_in_minutes',
                (
                    'are_stocks_displayed',
                    'is_hidden',
                    'can_be_purchased',
                    'is_balance_only',
                ),
            ),
        }),
    )

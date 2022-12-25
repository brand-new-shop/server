from django.urls import path
from products.views import (
    categories_list_view,
    category_products_list_view,
    subcategories_list_view,
    CategoryRetrieveView,
    ProductRetrieveView,
)

urlpatterns = [
    path('categories/', categories_list_view),
    path('categories/<int:category_id>/', CategoryRetrieveView.as_view()),
    path('categories/<int:category_id>/products/', category_products_list_view),
    path('categories/<int:category_id>/subcategories/', subcategories_list_view),
    path('categories/products/<int:product_id>/', ProductRetrieveView.as_view()),
]

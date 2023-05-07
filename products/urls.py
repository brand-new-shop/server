from django.urls import path
from products.views import (
    ProductRetrieveApi,
    CategoryListApi,
    CategoryRetrieveApi,
    ProductListApi,
)

urlpatterns = [
    path('categories/', CategoryListApi.as_view()),
    path('categories/<int:category_id>/', CategoryRetrieveApi.as_view()),
    path('categories/<int:category_id>/products/', ProductListApi.as_view()),
    path('categories/products/<int:product_id>/', ProductRetrieveApi.as_view()),
]

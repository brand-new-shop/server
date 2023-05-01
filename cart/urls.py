from django.urls import path

from cart.views import (
    CartProductListCreateApi,
    CartProductRetrieveUpdateDeleteApi,
    OrderCreateApi,
)

urlpatterns = [
    path('users/<int:telegram_id>/', CartProductListCreateApi.as_view()),
    path(
        '<int:cart_product_id>/',
        CartProductRetrieveUpdateDeleteApi.as_view(),
    ),
    path('users/<int:telegram_id>/orders/', OrderCreateApi.as_view()),
]

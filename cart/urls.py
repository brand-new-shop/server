from django.urls import path

from cart.views import CartProductListCreateView, CartProductDetailView

urlpatterns = [
    path('users/<int:telegram_id>/', CartProductListCreateView.as_view()),
    path('<int:cart_product_id>/', CartProductDetailView.as_view()),
]

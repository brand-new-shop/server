from django.db import IntegrityError, DatabaseError
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_user_or_raise_404
from cart.services import create_cart_product, get_cart_product_or_raise_404, delete_cart_product, \
    update_cart_product_quantity
from products.services import get_product_or_raise_404
from cart.exceptions import NotEnoughProductStocks, ProductAlreadyExistsInCart
from cart.models import CartProduct
from cart.serializers import CartProductCreateSerializer, CartProductQuantityChangeSerializer


class CartProductListCreateView(APIView):

    def get(self, request, telegram_id: int):
        cart_products = (
            CartProduct.objects
            .select_related('user', 'product')
            .filter(user__telegram_id=telegram_id)
            .values('id', 'product__id', 'product__name', 'quantity', 'product__price')
        )
        response_data = [
            {
                'cart_product_id': cart_product['id'],
                'product_id': cart_product['product__id'],
                'product_name': cart_product['product__name'],
                'product_price': cart_product['product__price'],
                'quantity': cart_product['quantity'],
            }
            for cart_product in cart_products
        ]
        return Response(response_data)

    def post(self, request, telegram_id: int):
        serializer = CartProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        product_id, quantity = serialized_data['product_id'], serialized_data['quantity']

        user = get_user_or_raise_404(telegram_id)
        product = get_product_or_raise_404(product_id)

        cart_product = create_cart_product(user, product, quantity)

        response_data = {
            'cart_product_id': cart_product.id,
            'product_id': cart_product.product.id,
            'product_name': cart_product.product.name,
            'product_price': cart_product.product.price,
            'quantity': cart_product.quantity,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class CartProductDetailView(APIView):

    def get(self, request, cart_product_id: int):
        cart_product = get_cart_product_or_raise_404(cart_product_id)
        response_data = {
            'cart_product_id': cart_product.id,
            'product_id': cart_product.product.id,
            'product_name': cart_product.product.name,
            'product_price': cart_product.product.price,
            'quantity': cart_product.quantity,
        }
        return Response(response_data)

    def delete(self, request, cart_product_id: int):
        cart_product = get_cart_product_or_raise_404(cart_product_id)
        delete_cart_product(cart_product)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, cart_product_id: int):
        serializer = CartProductQuantityChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_product = get_cart_product_or_raise_404(cart_product_id)
        update_cart_product_quantity(cart_product, serializer.data['quantity'])
        return Response(status.HTTP_204_NO_CONTENT)

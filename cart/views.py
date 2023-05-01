from rest_framework import status, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_user_or_raise_404
from cart.models import CartProduct
from cart.services import (
    create_cart_product,
    get_cart_product_or_raise_404,
    delete_cart_product,
    update_cart_product_quantity,
)
from core.serializers import LimitOffsetSerializer
from products.services import get_product_or_raise_404


class CartProductListCreateApi(APIView):

    class OutputSerializer(serializers.Serializer):
        cart_product_id = serializers.IntegerField(source='id')
        product_id = serializers.IntegerField(source='product.id')
        product_name = serializers.CharField(source='product.name')
        product_price = serializers.DecimalField(
            source='product.price',
            max_digits=10,
            decimal_places=2,
        )
        quantity = serializers.IntegerField()

    class InputCreateSerializer(serializers.Serializer):
        product_id = serializers.IntegerField(min_value=1)
        quantity = serializers.IntegerField(min_value=1)

    def get(self, request: Request, telegram_id: int):
        serializer = LimitOffsetSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        limit: int = serialized_data['limit']
        offset: int = serialized_data['offset']
        cart_products = (
            CartProduct.objects
            .select_related('product')
            .filter(user__telegram_id=telegram_id)[offset:limit + offset + 1]
            .only('id', 'product__id', 'product__name', 'quantity',
                  'product__price')
        )
        is_end_of_list_reached = len(cart_products) <= limit
        cart_products = cart_products[:limit]
        serializer = self.OutputSerializer(cart_products, many=True)
        response_data = {
            'cart_products': serializer.data,
            'is_end_of_list_reached': is_end_of_list_reached,
        }
        return Response(response_data)

    def post(self, request, telegram_id: int):
        serializer = self.InputCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        product_id: int = serialized_data['product_id']
        quantity: int = serialized_data['quantity']

        user = get_user_or_raise_404(telegram_id)
        product = get_product_or_raise_404(product_id)

        cart_product = create_cart_product(user, product, quantity)

        serializer = self.OutputSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartProductRetrieveUpdateDeleteApi(APIView):

    class InputSerializer(serializers.Serializer):
        quantity = serializers.IntegerField(min_value=1)

    class OutputSerializer(serializers.Serializer):
        cart_product_id = serializers.IntegerField(source='id')
        product_id = serializers.IntegerField(source='product.id')
        product_name = serializers.CharField(source='product.name')
        product_price = serializers.DecimalField(
            source='product.price',
            max_digits=10,
            decimal_places=2,
        )
        quantity = serializers.IntegerField()

    def get(self, request, cart_product_id: int):
        cart_product = get_cart_product_or_raise_404(cart_product_id)
        serializer = self.OutputSerializer(cart_product)
        return Response(serializer.data)

    def delete(self, request, cart_product_id: int):
        cart_product = get_cart_product_or_raise_404(cart_product_id)
        delete_cart_product(cart_product)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, cart_product_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity: int = serializer.data['quantity']
        cart_product = get_cart_product_or_raise_404(cart_product_id)
        update_cart_product_quantity(cart_product, quantity)
        return Response(status=status.HTTP_204_NO_CONTENT)

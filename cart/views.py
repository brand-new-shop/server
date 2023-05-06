from django.db.models import Sum, F, Count
from rest_framework import status, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_user_or_raise_404
from cart.models import CartProduct, OrderProduct, Order
from cart.services import (
    create_cart_product,
    get_cart_product_or_raise_404,
    delete_cart_product,
    update_cart_product_quantity,
    create_order,
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


class OrderCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        payment_type = serializers.CharField(min_length=1, max_length=255)

    class OutputListSerializer(serializers.Serializer):
        class OrderProductSerializer(serializers.ModelSerializer):
            product_id = serializers.IntegerField(source='product.id')
            product_name = serializers.CharField(source='product.name')

            class Meta:
                model = OrderProduct
                exclude = ('order', 'id', 'product')

        id = serializers.IntegerField()
        payment_type = serializers.CharField()
        created_at = serializers.DateTimeField()
        products = OrderProductSerializer(many=True, source='orderproduct_set')

    class OutputCreateSerializer(serializers.Serializer):
        class OrderProductSerializer(serializers.ModelSerializer):
            product_id = serializers.IntegerField(source='product.id')
            product_name = serializers.CharField(source='product.name')

            class Meta:
                model = OrderProduct
                exclude = ('order', 'id', 'product')

        order_id = serializers.IntegerField(source='order.id')
        payment_type = serializers.CharField(source='order.payment_type')
        created_at = serializers.DateTimeField(source='order.created_at')
        products = OrderProductSerializer(many=True)

    def get(self, request: Request, telegram_id: int):
        user_orders = (
            Order.objects
            .prefetch_related('orderproduct_set')
            .filter(user__telegram_id=telegram_id)
        )
        serializer = self.OutputListSerializer(user_orders, many=True)
        response_data = {
            'orders': serializer.data,
        }
        return Response(response_data)

    def post(self, request: Request, telegram_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        payment_type: str = serialized_data['payment_type']

        user = get_user_or_raise_404(telegram_id)
        created_order = create_order(user, payment_type)
        serializer = self.OutputCreateSerializer(created_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdersStatisticsApi(APIView):

    class OutputSerializer(serializers.Serializer):
        total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
        total_count = serializers.IntegerField()

    def get(self, request: Request, telegram_id: int):
        orders_statistics = (
            Order.objects
            .filter(user__telegram_id=telegram_id)
            .aggregate(
                total_cost=Sum(
                    F('orderproduct__quantity')
                    * F('orderproduct__product_price_at_the_moment'),
                    default=0,
                ),
                total_count=Count('id'),
            )
        )
        serializer = self.OutputSerializer(orders_statistics)
        return Response(serializer.data)

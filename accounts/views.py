from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import (
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)
from products.models import Order, Product


@api_view(['POST'])
def user_create_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serialized_data = serializer.data
    try:
        user = User.objects.create(telegram_id=serialized_data['telegram_id'], username=serialized_data['username'])
    except IntegrityError:
        raise APIException('User already exists', status.HTTP_409_CONFLICT)
    serializer = UserRetrieveSerializer(user)
    return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):

    def get(self, request, telegram_id: int):
        user = get_object_or_404(User, telegram_id=telegram_id)
        serializer = UserRetrieveSerializer(user)
        return Response(serializer.data)

    def patch(self, request, telegram_id: int):
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        is_updated = User.objects.filter(telegram_id=telegram_id).update(username=serialized_data['username'])
        if not is_updated:
            raise NotFound('User by Telegram ID is not found')
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrdersListCreateView(APIView):

    def get(self, request, telegram_id: int):
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))
        orders = (
            Order.objects
            .select_related('user')
            .select_related('product')
            .filter(user__telegram_id=telegram_id)
            .order_by('-created_at')
            .values('id', 'product__name', 'quantity', 'total_price')[offset:offset + limit]
        )
        response_data = [{'id': order['id'], 'product_name': order['product__name'],
                          'quantity': order['quantity'], 'total_price': order['total_price']}
                         for order in orders]
        return Response(response_data)


@api_view(['GET'])
def orders_count_view(request, telegram_id: int):
    orders_count = Order.objects.select_related('user').filter(user__telegram_id=telegram_id).count()
    return Response({'user_telegram_id': telegram_id, 'orders_total_count': orders_count})


@api_view(['GET'])
def orders_statistics_view(request, telegram_id: int):
    orders = (
        Order.objects
        .select_related('user')
        .filter(user__telegram_id=telegram_id)
        .values('quantity', 'total_price')
    )
    orders_count = sum(order['quantity'] for order in orders)
    orders_total_price = sum(order['total_price'] for order in orders)
    response_data = {
        'user_telegram_id': telegram_id,
        'orders_count': orders_count,
        'orders_total_price': orders_total_price,
    }
    return Response(response_data)

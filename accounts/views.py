from rest_framework import status, serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.services import create_user, update_username


class UserRetrieveSerializerMixin:

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                'telegram_id',
                'username',
                'is_banned',
                'created_at',
                'balance',
            )


class UserCreateApi(APIView, UserRetrieveSerializerMixin):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('telegram_id', 'username')

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        telegram_id: int = serialized_data['telegram_id']
        username: str | None = serialized_data['username']
        user = create_user(telegram_id, username)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserRetrieveUpdateApi(APIView, UserRetrieveSerializerMixin):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username',)

    def get(self, request, telegram_id: int):
        user = get_object_or_404(User, telegram_id=telegram_id)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)

    def patch(self, request, telegram_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        username: str | None = serialized_data['username']
        is_updated = update_username(telegram_id, username)
        if not is_updated:
            raise NotFound('User by Telegram ID is not found')
        return Response(status=status.HTTP_204_NO_CONTENT)

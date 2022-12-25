from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserCreateSerializer, UserRetrieveSerializer, UserUpdateSerializer


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

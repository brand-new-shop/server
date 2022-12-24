from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
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
    user, is_created = User.objects.get_or_create(telegram_id=serialized_data['telegram_id'],
                                                  username=serialized_data['username'])
    serializer = UserRetrieveSerializer(user)
    response_status = status.HTTP_201_CREATED if is_created else status.HTTP_409_CONFLICT
    response_data = serializer.data | {'is_created': is_created}
    return Response(response_data, response_status)


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

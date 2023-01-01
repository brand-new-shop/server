from django.utils.text import Truncator
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from support.models import SupportTicket
from support.serializers import SupportRequestCreateSerializer, SupportRequestSerializer


class SupportRequestListCreateView(APIView):

    def get(self, request, user_telegram_id: int):
        support_requests = (
            SupportTicket.objects
            .select_related('user')
            .filter(user__telegram_id=user_telegram_id)
            .values('id', 'issue')
        )
        response_data = [{'id': support_request['id'],
                          'issue_preview': Truncator(support_request['issue']).words(num=10, truncate='...')}
                         for support_request in support_requests]
        return Response(response_data)

    def post(self, request, user_telegram_id: int):
        serializer = SupportRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids = User.objects.filter(telegram_id=user_telegram_id).values_list('id', flat=True)
        if not user_ids:
            raise NotFound('User by Telegram ID is not found')

        serialized_data = serializer.data
        support_request = SupportTicket.objects.create(
            user_id=user_ids[0],
            issue=serialized_data['issue'],
            subject_id=serialized_data['subject_id'],
        )
        response_data = {'id': support_request.id}
        return Response(response_data, status=status.HTTP_201_CREATED)


class SupportRequestRetrieveView(RetrieveAPIView):
    serializer_class = SupportRequestSerializer
    queryset = SupportTicket.objects.all()
    lookup_url_kwarg = 'support_request_id'

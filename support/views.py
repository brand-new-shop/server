from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from support.models import SupportTicket
from support.serializers import SupportTicketCreateSerializer, SupportTicketSerializer


class SupportTicketListCreateView(APIView):

    def get(self, request, telegram_id: int):
        support_requests = (
            SupportTicket.objects
            .select_related('user')
            .filter(user__telegram_id=telegram_id)
            .values('id', 'status', 'subject')
        )
        if not support_requests:
            raise NotFound("User's tickets have not found")
        response_data = [
            {
                'id': request['id'],
                'status': SupportTicket.Status(request['status']).label,
                'subject': request['subject']
            }
            for request in support_requests
        ]
        return Response(response_data)

    def post(self, request, telegram_id: int):
        serializer = SupportTicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, telegram_id=telegram_id)
        serialized_data = serializer.data
        support_ticket = SupportTicket.objects.create(
            user=user,
            issue=serialized_data['issue'],
            subject=serialized_data['subject']
        )
        response_data = {'id': support_ticket.id}
        return Response(response_data, status=status.HTTP_201_CREATED)


class SupportTicketRetrieveView(RetrieveAPIView):
    serializer_class = SupportTicketSerializer
    queryset = SupportTicket.objects.all()
    lookup_url_kwarg = 'ticket_id'

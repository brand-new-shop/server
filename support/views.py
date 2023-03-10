from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from support.exceptions import SupportTicketCreationRateLimitExceeded, TicketIsClosed
from support.models import SupportTicket, ReplyToTicket
from support.serializers import (
    SupportTicketCreateSerializer,
    SupportTicketSerializer,
    ReplyToTicketCreateSerializer,
    ReplyToTicketSerializer,
)


class SupportTicketListCreateView(APIView):

    def get(self, request, telegram_id: int):
        support_requests = (
            SupportTicket.objects
            .select_related('user')
            .filter(user__telegram_id=telegram_id)
            .order_by('-created_at')
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
        last_ticket_created_at = (
            SupportTicket.objects
            .filter(user=user)
            .order_by('-created_at')
            .values_list('created_at', flat=True)
            .first()
        )
        if last_ticket_created_at is not None:
            passed_seconds_since_last_ticket = (timezone.now() - last_ticket_created_at).total_seconds()
            seconds_to_wait = int(settings.TICKET_CREATION_DELAY_IN_SECONDS - passed_seconds_since_last_ticket)
            if seconds_to_wait > 0:
                raise SupportTicketCreationRateLimitExceeded(seconds_to_wait)
        support_ticket = SupportTicket.objects.create(
            user=user,
            issue=serialized_data['issue'],
            subject=serialized_data['subject']
        )
        response_data = {'id': support_ticket.id}
        return Response(response_data, status=status.HTTP_201_CREATED)


class SupportTicketRetrieveUpdateView(RetrieveAPIView):
    serializer_class = SupportTicketSerializer
    queryset = SupportTicket.objects.all()
    lookup_url_kwarg = 'ticket_id'

    def patch(self, request, ticket_id: int):
        updated_rows_count = SupportTicket.objects.filter(id=ticket_id).update(status=SupportTicket.Status.CLOSED)
        if not updated_rows_count:
            raise NotFound('Ticket is not found')
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyToTicketListCreateView(APIView):

    def get(self, request, ticket_id: int):
        reply_ids = (
            ReplyToTicket.objects
            .filter(ticket_id=ticket_id)
            .values_list('id', flat=True)
            .order_by('created_at')
        )
        return Response(reply_ids)

    def post(self, request, ticket_id: int):
        serializer = ReplyToTicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        support_ticket = get_object_or_404(SupportTicket, id=ticket_id)
        if support_ticket.status == SupportTicket.Status.CLOSED:
            raise TicketIsClosed
        reply_to_ticket = ReplyToTicket.objects.create(ticket=support_ticket, issue=serialized_data['issue'])
        return Response({'id': reply_to_ticket.id}, status=status.HTTP_201_CREATED)


class ReplyToTicketRetrieveView(RetrieveAPIView):
    serializer_class = ReplyToTicketSerializer
    queryset = ReplyToTicket.objects.all()
    lookup_url_kwarg = 'reply_id'

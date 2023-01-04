from rest_framework import serializers

from support.models import SupportTicket, ReplyToTicket


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ('subject', 'issue')


class SupportTicketSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = SupportTicket
        fields = ('id', 'created_at', 'status', 'issue', 'answer', 'subject')


class ReplyToTicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToTicket
        fields = ('issue',)


class ReplyToTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToTicket
        fields = ('id', 'created_at', 'issue', 'answer', 'ticket')
        depth = 1

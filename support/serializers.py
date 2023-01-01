from rest_framework import serializers

from support.models import SupportTicket


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ('subject', 'issue')


class SupportTicketSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = SupportTicket
        fields = ('id', 'created_at', 'status', 'issue', 'answer', 'subject')

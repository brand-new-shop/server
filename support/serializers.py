from rest_framework import serializers

from support.models import SupportSubject, SupportRequest


class SupportSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportSubject
        fields = '__all__'


class SupportRequestCreateSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()
    issue = serializers.CharField(max_length=4096)


class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ('id', 'created_at', 'is_open', 'issue', 'answer', 'subject')
        depth = 1

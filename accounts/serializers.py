from rest_framework import serializers


class UserRetrieveSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(allow_null=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_banned = serializers.BooleanField()


class UserCreateSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(max_length=64, allow_null=True, allow_blank=True, default=None)


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)

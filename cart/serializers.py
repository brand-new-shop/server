from rest_framework import serializers

from cart.models import CartProduct


class CartProductCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CartProductQuantityChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('quantity',)

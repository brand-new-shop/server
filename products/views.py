from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import LimitOffsetSerializer
from products.models import Category, Product


class CategoryListApi(APIView):

    class InputSerializer(LimitOffsetSerializer):
        parent_id = serializers.IntegerField(
            min_value=1,
            allow_null=True,
            default=None,
        )

    def get(self, request: Request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        limit: int = serialized_data['limit']
        offset: int = serialized_data['offset']
        parent_id: int | None = serialized_data['parent_id']

        categories = (
            Category.objects
            .filter(is_hidden=False, parent_id=parent_id)
            .order_by('-priority')[offset:limit + offset + 1]
            .values('id', 'name', 'emoji_icon')
        )
        is_end_of_list_reached = len(categories) <= limit
        response_data = {
            'categories': categories[:limit],
            'is_end_of_list_reached': is_end_of_list_reached,
        }
        return Response(response_data)


class ProductListApi(APIView):

    def get(self, request: Request, category_id: int):
        serializer = LimitOffsetSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        limit: int = serialized_data['limit']
        offset: int = serialized_data['offset']

        products = (
            Product.objects
            .filter(
                category_id=category_id,
                is_hidden=False,
            )[offset:limit + offset + 1]
            .values('id', 'name')
        )
        is_end_of_list_reached = len(products) <= limit
        response_data = {
            'products': products[:limit],
            'is_end_of_list_reached': is_end_of_list_reached,
        }
        return Response(response_data)


class CategoryRetrieveApi(RetrieveAPIView):
    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = (
                'id',
                'name',
                'emoji_icon',
                'parent',
                'is_hidden',
                'created_at'
            )

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'category_id'


class ProductRetrieveApi(APIView):

    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Product
            fields = '__all__'
            depth = 1

    def get(self, request: Request, product_id: int):
        product = Product.objects.prefetch_related('productpicture_set').get(id=product_id)
        picture_urls = product.productpicture_set.values_list('url', flat=True)
        response_data = self.OutputSerializer(product).data | {'picture_urls': picture_urls}
        return Response(response_data)

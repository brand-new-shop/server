from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer


@api_view(['GET'])
def categories_list_view(request):
    categories = (
        Category.objects
        .filter(is_hidden=False, parent=None)
        .order_by('priority')
        .values('id', 'name', 'emoji_icon')
    )
    return Response(categories)


@api_view(['GET'])
def category_products_list_view(request, category_id: int):
    products = Product.objects.filter(category_id=category_id).values('id', 'name')
    return Response(products)


@api_view(['GET'])
def subcategories_list_view(request, category_id: int):
    subcategories = (
        Category.objects
        .filter(parent_id=category_id, is_hidden=False)
        .order_by('priority')
        .values('id', 'name', 'emoji_icon')
    )
    return Response(subcategories)


class CategoryRetrieveView(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'category_id'


class ProductRetrieveView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg = 'product_id'

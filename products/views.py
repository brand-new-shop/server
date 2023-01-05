from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from products.models import Category, Product, ProductPicture
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
    products = Product.objects.filter(category_id=category_id, is_hidden=False).values('id', 'name')
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


@api_view(['GET'])
def product_retrieve_view(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    picture_urls = product.productpicture_set.values_list('picture', flat=True)
    picture_urls = [settings.MEDIA_URL + url for url in picture_urls]
    response_data = ProductSerializer(product).data | {'picture_urls': picture_urls}
    return Response(response_data)

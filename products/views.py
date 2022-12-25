from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Category, Product


@api_view(['GET'])
def categories_list_view(request):
    categories = Category.objects.filter(is_hidden=False).filter(parent=None).values('id', 'name', 'emoji_icon')
    return Response(categories)


def category_products_list_view(request, category_id: int):
    products = Product.objects.filter(category_id=category_id).values('id', 'name')


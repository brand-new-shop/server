from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from info.models import ShopInfo


@api_view(['GET'])
def shop_info_view(request, info_key: str):
    shop_info = get_object_or_404(ShopInfo, key=info_key)
    return Response({'key': shop_info.key, 'value': shop_info.value})

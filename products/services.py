from products.models import Product
from products.exceptions import ProductNotFound

__all__ = ('get_product_or_raise_404',)


def get_product_or_raise_404(product_id: int) -> Product:
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ProductNotFound

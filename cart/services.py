from django.db import transaction, IntegrityError

from accounts.models import User
from cart.exceptions import CartProductNotFound, NotEnoughProductStocks, ProductAlreadyExistsInCart
from cart.models import CartProduct
from products.models import Product

__all__ = ('create_cart_product', 'get_cart_product_or_raise_404', 'delete_cart_product')


@transaction.atomic
def create_cart_product(user: User, product: Product, quantity: int) -> CartProduct:
    if product.stocks_count < quantity:
        raise NotEnoughProductStocks
    try:
        cart_product = CartProduct.objects.create(user=user, product=product, quantity=quantity)
    except IntegrityError:
        raise ProductAlreadyExistsInCart
    product.stocks_count -= quantity
    product.save()
    return cart_product


@transaction.atomic
def delete_cart_product(cart_product: CartProduct):
    product = cart_product.product
    product.stocks_count += cart_product.quantity
    product.save()
    cart_product.delete()


@transaction.atomic
def update_cart_product_quantity(cart_product: CartProduct, quantity: int):
    product = cart_product.product
    cart_product_quantity_change = quantity - cart_product.quantity
    if product.stocks_count < cart_product_quantity_change:
        raise NotEnoughProductStocks
    product.stocks_count -= cart_product_quantity_change
    cart_product.quantity = quantity
    cart_product.save()
    product.save()


def get_cart_product_or_raise_404(cart_product_id: int) -> CartProduct:
    cart_product = CartProduct.objects.select_related('product').filter(id=cart_product_id).first()
    if cart_product is None:
        raise CartProductNotFound
    return cart_product

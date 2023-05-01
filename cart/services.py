from dataclasses import dataclass

from django.db import transaction, IntegrityError

from accounts.models import User
from cart.exceptions import (
    CartProductNotFound, NotEnoughProductStocks,
    ProductAlreadyExistsInCart
)
from cart.models import CartProduct, Order, OrderProduct
from products.models import Product

__all__ = (
    'create_cart_product', 'get_cart_product_or_raise_404',
    'delete_cart_product'
)


@dataclass(frozen=True, slots=True)
class CreatedOrder:
    order: Order
    products: list[OrderProduct]


@transaction.atomic
def create_cart_product(user: User, product: Product,
                        quantity: int) -> CartProduct:
    if product.stocks_count < quantity:
        raise NotEnoughProductStocks
    try:
        cart_product = CartProduct.objects.create(user=user, product=product,
                                                  quantity=quantity)
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
    cart_product = CartProduct.objects.select_related('product').filter(
        id=cart_product_id).first()
    if cart_product is None:
        raise CartProductNotFound
    return cart_product


@transaction.atomic
def create_order(user: User, payment_type: str) -> CreatedOrder:
    order = Order.objects.create(user=user, payment_type=payment_type)
    user_cart_products = user.cartproduct_set.select_related('product')
    order_products = [
        OrderProduct(
            order=order,
            product=cart_product.product,
            quantity=cart_product.quantity,
            product_price_at_the_moment=cart_product.product.price,
        ) for cart_product in user_cart_products
    ]
    created_order_products = OrderProduct.objects.bulk_create(order_products)
    return CreatedOrder(
        order=order,
        products=created_order_products,
    )

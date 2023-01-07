from django.test import TestCase

from accounts.models import User
from products.models import Product, Category
from cart.services import create_cart_product, delete_cart_product, update_cart_product_quantity


class CartProductTestCase(TestCase):

    def setUp(self) -> None:
        category = Category.objects.create(name='Fruit', priority=1)
        self.stocks_count = 10
        self.product = Product.objects.create(
            category=category,
            name='Apple',
            description='A green apple',
            price=5.5,
            stocks_count=self.stocks_count,
            content='Hello',
        )
        self.user = User.objects.create(telegram_id=123456789)


class TestCreateCartProduct(CartProductTestCase):

    def test_card_product_created(self) -> None:
        self.assertEqual(self.product.stocks_count, 10)
        create_cart_product(self.user, self.product, quantity=3)
        self.assertEqual(self.product.stocks_count, 7)


class TestDeleteCartProduct(CartProductTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.cart_product = create_cart_product(self.user, self.product, quantity=5)

    def test_cart_product_deleted(self) -> None:
        self.assertEqual(self.product.stocks_count, 5)
        delete_cart_product(self.cart_product)
        self.assertEqual(self.product.stocks_count, 10)


class TestUpdateCardProductQuantity(CartProductTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.product.refresh_from_db()

    def test_card_product_update_quantity(self):
        cart_product = create_cart_product(self.user, self.product, quantity=5)
        self.assertEqual(self.product.stocks_count, 5)
        update_cart_product_quantity(cart_product, 6)
        self.assertEqual(cart_product.quantity, 6)
        self.assertEqual(self.product.stocks_count, 4)

        cart_product = create_cart_product(self.user, self.product, quantity=5)
        self.assertEqual(self.product.stocks_count, 5)
        update_cart_product_quantity(cart_product, 4)
        self.assertEqual(cart_product.quantity, 4)
        self.assertEqual(self.product.stocks_count, 6)

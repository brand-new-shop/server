from rest_framework.exceptions import NotFound


class ProductNotFound(NotFound):
    default_detail = 'Product is not found'

from django.urls import path
from products.views import categories_list_view

urlpatterns = [
    path('categories/', categories_list_view),
]

from django.urls import path
from info.views import shop_info_view

urlpatterns = [
    path('info/<str:info_key>/', shop_info_view),
]

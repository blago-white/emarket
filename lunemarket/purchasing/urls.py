from django.urls import path
from .views import ShoppingBasketView, AddProductToBasket, BuyProductView, DeleteProductFromBucketView

urlpatterns = [
    path('basket/<pk>', ShoppingBasketView.as_view(), name="basket"),
    path('bucket/add/<pk>/<str:productid>', AddProductToBasket.as_view(), name="save-product"),
    path('bucket/buy/<pk>/<str:productid>', BuyProductView.as_view(), name="buy-product"),
    path('bucket/delete/<pk>/<str:productid>', DeleteProductFromBucketView.as_view(), name="delete-product"),
]

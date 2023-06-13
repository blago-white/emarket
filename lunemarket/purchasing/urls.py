from django.urls import path
from .views import ShoppingBasketView, AddProductToBasketView, BuyProductView, DeleteProductFromBucketView

urlpatterns = [
    path('basket', ShoppingBasketView.as_view(), name="basket"),
    path('bucket/add/<str:productid>', AddProductToBasketView.as_view(), name="save-product"),
    path('bucket/buy/<int:pk>', BuyProductView.as_view(), name="buy-product"),
    path('bucket/delete/<int:pk>', DeleteProductFromBucketView.as_view(), name="delete-basket-product"),
]

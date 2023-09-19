from django.urls import path

from .views import ShoppingBasketView, AddProductToBasketView, BuyProductView, DeleteProductFromBasketView

urlpatterns = [
    path('', ShoppingBasketView.as_view(), name="basket"),
    path('add/<str:productid>', AddProductToBasketView.as_view(), name="save-product"),
    path('buy/<int:pk>', BuyProductView.as_view(), name="buy-product"),
    path('delete/<int:pk>', DeleteProductFromBasketView.as_view(), name="delete-basket-product"),
]

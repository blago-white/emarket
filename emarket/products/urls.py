from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page

from .views import (HomePageProductsView,
                    ProductsView,
                    ProductDetailView,
                    AddProductView,
                    DeleteUserProductView,
                    EditProductView,
                    ProductDoesNotExistWarningView)

urlpatterns = [
    path('', cache_page(settings.SHORT_CACHE_TIMEOUT)(
        HomePageProductsView.as_view()
    ), name="home"),
    path('products/category/<str:category>/', ProductsView.as_view(), name="category-products"),
    path('products/card/<int:pk>/', ProductDetailView.as_view(), name="product-card"),
    path('products/create/product/', AddProductView.as_view(), name="add-product"),
    path('products/edit/product/<int:pk>', EditProductView.as_view(), name="edit-product"),
    path('products/delete/product/<int:pk>', DeleteUserProductView.as_view(), name="delete-product"),
    path('products/notexist', cache_page(settings.LONG_CACHE_TIMEOUT)(
             ProductDoesNotExistWarningView.as_view()
         ), name="product-not-exist")
]

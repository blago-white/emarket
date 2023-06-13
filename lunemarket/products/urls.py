from django.urls import path
from .views import (ProductsView,
                    ProductDetailView,
                    AddProductView,
                    DeleteUserProduct,
                    EditProductView)

urlpatterns = [
    path('category/<str:category>/', ProductsView.as_view(), name="category-products"),
    path('card/<int:pk>/', ProductDetailView.as_view(), name="product-card"),
    path('create/product/', AddProductView.as_view(), name="add-product"),
    path('edit/product/<int:pk>', EditProductView.as_view(), name="edit-product"),
    path('delete/product/<int:pk>', DeleteUserProduct.as_view(), name="delete-product"),
]

from django.urls import path
from .views import ProductsView

urlpatterns = [
    path('<str:category>/', ProductsView.as_view(), name="category-products")
]

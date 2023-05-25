from django.urls import path
from .views import ProductsView, CardView

urlpatterns = [
    path('category/<str:category>/', ProductsView.as_view(), name="category-products"),
    path('card/<str:title>/', CardView.as_view(), name="product-card")
]

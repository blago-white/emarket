from django.urls import path
from .views import ProductsView, CardView, AddProductView, AddCategoryView

urlpatterns = [
    path('category/<str:category>/', ProductsView.as_view(), name="category-products"),
    path('card/<str:title>/', CardView.as_view(), name="product-card"),
    path('create/card/', AddProductView.as_view(), name="add-card"),
    path('create/category/', AddCategoryView.as_view(), name="add-category")

]

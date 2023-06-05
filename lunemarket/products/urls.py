from django.urls import path
from .views import ProductsView, CardView, AddProductView, AddCategoryView, DeleteUserCard, DeleteUserCategory

urlpatterns = [
    path('category/<str:category>/', ProductsView.as_view(), name="category-products"),
    path('card/<str:title>/', CardView.as_view(), name="product-card"),
    path('create/card/', AddProductView.as_view(), name="add-card"),
    path('create/category/', AddCategoryView.as_view(), name="add-category"),
    path('delete/card/<str:title>', DeleteUserCard.as_view(), name="delete-user-card"),
    path('delete/category/<str:title>', DeleteUserCategory.as_view(), name="delete-user-category")
]

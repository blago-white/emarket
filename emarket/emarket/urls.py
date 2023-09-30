from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls")),
    path('accounts/', include('users.urls')),
    path('accounts/', include("allauth.urls")),
    path('backet/', include('purchasing.urls')),
]

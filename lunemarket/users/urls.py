from django.urls import path
from .views import RegisterUserView
from home.views import HomeView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('account/', HomeView.as_view(), name="account")
]

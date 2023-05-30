from django.urls import path
from .views import RegisterUserView, LoginUserView, AccountView, LogoutUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('login/', LoginUserView.as_view(), name="login"),
    path('account/<pk>', AccountView.as_view(), name="account"),
    path('logout/', LogoutUserView.as_view(), name="logout")
]

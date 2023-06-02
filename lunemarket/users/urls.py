from django.urls import path
from .views import RegisterUserView, LoginUserView, LogoutUserView, AccountInfoView, AccountCardsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('login/', LoginUserView.as_view(), name="login"),
    path('account/<pk>/info', AccountInfoView.as_view(), name="account-info"),
    path('account/<pk>/cards', AccountCardsView.as_view(), name="account-cards"),
    path('logout/', LogoutUserView.as_view(), name="logout")
]

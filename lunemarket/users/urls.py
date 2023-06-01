from django.urls import path
from .views import RegisterUserView, LoginUserView, AccountView, LogoutUserView, UserAccountCardsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('login/', LoginUserView.as_view(), name="login"),
    path('account/<pk>', AccountView.as_view(), name="account"),
    path('account/<pk>/info', AccountView.as_view(), name="account-info"),
    path('account/<pk>/cards', UserAccountCardsView.as_view(), name="account-cards"),
    path('logout/', LogoutUserView.as_view(), name="logout")
]

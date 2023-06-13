from django.urls import path
from .views import (RegisterUserView,
                    LoginUserView,
                    LogoutUserView,
                    AccountInfoView,
                    AccountProductsView,
                    AccountNotificationsView,
                    AccountNotificationDeleteView)

urlpatterns = [
    path('accounts/signup/', RegisterUserView.as_view(), name="register"),
    path('accounts/login/', LoginUserView.as_view(), name="login"),
    path('profile/notifications', AccountNotificationsView.as_view(), name="account-notifications"),
    path('profile/notifications/delete/<int:pk>', AccountNotificationDeleteView.as_view(),
         name="account-notification-delete"),
    path('profile/<int:pk>/info', AccountInfoView.as_view(), name="account-info"),
    path('profile/<int:pk>/cards', AccountProductsView.as_view(), name="account-products"),
    path('accounts/logout/', LogoutUserView.as_view(), name="logout")
]

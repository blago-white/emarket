from django.urls import path
from .views import (RegisterUserView,
                    LoginUserView,
                    LogoutUserView,
                    AccountInfoView,
                    AccountCardsView,
                    AccountCategoriesView,
                    AccountNotificationsView,
                    AccountNotificationDeleteView)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('login/', LoginUserView.as_view(), name="login"),
    path('account/notifications', AccountNotificationsView.as_view(), name="account-notifications"),
    path('account/notifications/delete/<pk>', AccountNotificationDeleteView.as_view(),
         name="account-notification-delete"),
    path('account/<pk>/info', AccountInfoView.as_view(), name="account-info"),
    path('account/<pk>/cards', AccountCardsView.as_view(), name="account-cards"),
    path('account/<pk>/categories', AccountCategoriesView.as_view(), name="account-categories"),
    path('logout/', LogoutUserView.as_view(), name="logout")
]

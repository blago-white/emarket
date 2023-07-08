from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('accounts/signup/', RegisterUserView.as_view(), name="register"),
    path('accounts/login/', LoginUserView.as_view(), name="login"),
    path('accounts/password/change/', UserPasswordChangeView.as_view(), name="account_change_password"),
    path('accounts/login/error/', UserLoginErrorView.as_view(), name="socialaccount_login_error"),
    path('accounts/change', ChangeAccountDataView.as_view(), name="change-account-field"),
    path('accounts/confirm-email/', UserEmailVerificationView.as_view(), name="account_email_verification_sent"),
    path('accounts/password/reset/', ResetUserPasswordView.as_view(), name="account_reset_password"),
    path('accounts/password/reset/done/', ResetUserPasswordDoneView.as_view(), name="account_reset_password_done"),
    path('accounts/notifications/delete/<int:pk>', AccountNotificationDeleteView.as_view(),
         name="account-notification-delete"),
    path('accounts/notifications', AccountNotificationsView.as_view(), name="account-notifications"),
    path('accounts/<int:pk>/info', AccountInfoView.as_view(), name="account-info"),
    path('accounts/<int:pk>/cards', AccountProductsView.as_view(), name="account-products"),
    path('accounts/logout/', LogoutUserView.as_view(), name="logout"),
    path('accounts/email/', RedirectToAccountInfoView.as_view(), name="account_email"),
    re_path(
        r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        ResetUserPasswordFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
]

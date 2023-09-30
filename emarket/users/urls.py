from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('about/', AboutInfoView.as_view(), name="about-emarket"),
    path('signup/', RegisterUserView.as_view(), name="register"),
    path('login/', LoginUserView.as_view(), name="login"),
    path('password/change/', UserPasswordChangeView.as_view(), name="account_change_password"),
    path('login/error/', UserLoginErrorView.as_view(), name="socialaccount_login_error"),
    path('change', ChangeAccountDataView.as_view(), name="change-account-field"),
    path('confirm-email/', UserEmailVerificationView.as_view(), name="account_email_verification_sent"),
    path('password/reset/', ResetUserPasswordView.as_view(), name="account_reset_password"),
    path('password/reset/done/', ResetUserPasswordDoneView.as_view(), name="account_reset_password_done"),
    path('notifications/delete/<int:pk>', AccountNotificationDeleteView.as_view(),
         name="account-notification-delete"),
    path('notifications', AccountNotificationsView.as_view(), name="account-notifications"),
    path('<int:pk>/info', AccountInfoView.as_view(), name="account-info"),
    path('<int:pk>/cards', AccountProductsView.as_view(), name="account-products"),
    path('logout/', LogoutUserView.as_view(), name="logout"),
    path('email/', RedirectToAccountInfoView.as_view(), name="account_email"),
    path('delivered/', DistributionDeliveredView.as_view(), name="distribution-delivered"),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        ResetUserPasswordFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
]

from allauth.account.views import PasswordResetView as AllauthPasswordResetView
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from emarket.testsutils import tests_presets, tests_utils
from emarket.testsutils.tests_presets import *

from . import *
from ..models.models import UserProfile, Notifications
from ..views import (LoginUserView,
                     UserPasswordChangeView,
                     AccountInfoView,
                     AccountProductsView,
                     AccountNotificationsView,
                     AccountNotificationDeleteView,
                     ChangeAccountDataView,
                     ResetUserPasswordView,
                     RedirectToAccountInfoView)


class _BaseNotificationsTestCase(tests_presets.BaseSingleUserTestCase):
    def create_notifications_for_user(self, test_user: User) -> None:
        Notifications(recipient=test_user,
                      theme="inf",
                      text="test notify").save()


class RegisterUserViewTestCase(TestCase):
    def test_form_valid(self):
        invalid_form_email_response = self.client.post(reverse("register"),
                                                       data={"email": "example",
                                                             "password1": TEST_USER_DEFAULT_PASSWORD,
                                                             "password2": TEST_USER_DEFAULT_PASSWORD})

        self.assertEqual(type(invalid_form_email_response), TemplateResponse)

        self.client.post(reverse("register"),
                         data={"email": TEST_USER_DEFAULT_EMAIL,
                               "password1": TEST_USER_DEFAULT_PASSWORD,
                               "password2": TEST_USER_DEFAULT_PASSWORD,
                               "user": AnonymousUser()})

        self.assertTrue(UserProfile.objects.all().exists() and User.objects.filter(username="example").exists())


class LoginUserViewTestCase(TestCase):
    def test_get_success_url(self):
        self.assertEqual(LoginUserView().get_success_url(), "/")

    def test_get_context_data(self):
        login_response = self.client.get(reverse("login"))

        for field_name in login_response.context_data["form"].fields:
            self.assertFalse(
                "placeholder" in login_response.context_data["form"].fields[field_name].widget.attrs.keys()
            )


class UserPasswordChangeViewTestCase(tests_presets.BaseSingleUserTestCase):
    request_factory: RequestFactory

    def test_get_context_data(self):
        request = self.get_request_with_test_user(request_method=self.request_factory.get,
                                                  path=reverse("account_change_password"))

        change_password_response = UserPasswordChangeView.as_view()(request)

        for field_name in change_password_response.context_data["form"].fields:
            self.assertFalse(
                "placeholder" in change_password_response.context_data["form"].fields[field_name].widget.attrs.keys()
            )


class AccountInfoViewTestCase(tests_presets.BaseTwinUsersTestCase):
    request_factory: RequestFactory
    _test_form_error = "testerror-errorfield"

    def test_get_object(self):
        self._test_account_info()
        self._test_account_info_form_errors()

    def _test_account_info_form_errors(self):
        self_account_info_request_with_error = self._get_test_self_account_info_request_with_form_error(
            test_user=self.first_test_user, error=self._test_form_error
        )

        account_info_form_error_response = AccountInfoView.as_view()(
            self_account_info_request_with_error,
            pk=self.first_test_user.id,
        )

        self.assertEqual(
            account_info_form_error_response.context_data["error"], self._test_form_error
        )
        self.assertEqual(
            account_info_form_error_response.context_data.get("error_field"), "errorfield"
        )
        self.assertEqual(
            account_info_form_error_response.context_data.get("error_name"), "testerror"
        )

    def _test_account_info(self):
        self_account_info_request = self._get_test_account_info_request(self.first_test_user)

        self.assertEqual(
            type(AccountInfoView.as_view()(
                self_account_info_request, pk=self.first_test_user.id
            ).context_data["object"]
                 ),
            User
        )

        self._create_test_user_profile(test_user=self.first_test_user)

        self.assertEqual(
            type(AccountInfoView.as_view()(
                self_account_info_request, pk=self.first_test_user.id
            ).context_data["object"]),
            UserProfile
        )

        stranger_account_info_request = self._get_test_account_info_request(
            test_user=self.first_test_user,
            account_info_pk=self.second_test_user.id
        )

        stranger_account_info_response = AccountInfoView.as_view()(
            stranger_account_info_request, pk=self.second_test_user.id
        )
        self.assertFalse(stranger_account_info_response.context_data.get("is_self_account"))
        self.assertEqual(type(stranger_account_info_response.context_data["object"]), User)

    def _create_test_user_profile(self, test_user: User):
        test_userprofile = UserProfile(user=test_user)
        test_userprofile.save()

    def _get_test_self_account_info_request_with_form_error(self, test_user: int, error: str) -> WSGIRequest:
        test_self_account_info_request = self.request_factory.get(
            reverse("account-info", kwargs={"pk": test_user.id}) + "?error=" + error
        )

        test_self_account_info_request.user = test_user

        return test_self_account_info_request

    def _get_test_account_info_request(self, test_user: User, account_info_pk: int = None) -> WSGIRequest:
        request = self.request_factory.get(
            reverse("account-info", kwargs={"pk": account_info_pk or test_user.id})
        )

        request.user = test_user

        return request


class AccountProductsViewTestCase(tests_presets.BaseTwinUsersTestCase):
    request_factory: RequestFactory

    def test_get_queryset(self):
        self._test_get_query_set_stranger_user()

    def _test_get_query_set_stranger_user(self):
        request = self.request_factory.get(reverse("account-products", kwargs={"pk": self.first_test_user.id}))
        request.user = self.first_test_user

        self._create_test_phones_for_user(test_user=self.first_test_user)

        self.assertEqual(
            AccountProductsView.as_view()(request, pk=self.first_test_user.id).context_data["items"].count(),
            2
        )

        request.user = self.second_test_user

        self.assertEqual(
            AccountProductsView.as_view()(request, pk=self.first_test_user.id).context_data["items"].count(),
            2
        )

    def _create_test_phones_for_user(self, test_user: User) -> None:
        test_category = tests_utils.create_default_test_category()

        tests_utils.create_test_product(test_user=test_user, test_category=test_category)
        tests_utils.create_test_product(test_user=test_user,
                                        test_category=test_category,
                                        products_count=10,
                                        title="test-product-second")


class AccountNotificationsViewTestCase(_BaseNotificationsTestCase):
    request_factory: RequestFactory
    test_user: User

    def test_get_context_data(self):
        request = self.get_request_with_test_user(request_method=self.request_factory.get,
                                                  path=reverse("account-notifications"))

        super().create_notifications_for_user(test_user=self.test_user)

        notifications_response = AccountNotificationsView.as_view()(request)
        self.assertEqual(notifications_response.context_data["notifications"].count(), 1)
        self.assertTrue(notifications_response.context_data["is_self_account"])


class AccountNotificationDeleteViewTestCase(_BaseNotificationsTestCase):
    request_factory: RequestFactory
    test_user: User

    def test_get_object(self):
        super().create_notifications_for_user(test_user=self.test_user)
        test_notification_id = Notifications.objects.all().values("id")[0]["id"]

        notification_delete_view = AccountNotificationDeleteView()
        notification_delete_view.kwargs = {"pk": test_notification_id}

        self.assertEqual(notification_delete_view.get_object(),
                         Notifications.objects.get(pk=test_notification_id))


class ChangeAccountDataViewTestCase(tests_presets.BaseSingleUserTestCase):
    _new_username = "testusernameChanged"
    request_factory: RequestFactory
    test_user: User

    def test_post(self):
        change_username_field_request = self.request_factory.post("change-account-field",
                                                                  data={"username": self._new_username})
        change_username_field_request.user = self.test_user
        ChangeAccountDataView.as_view()(change_username_field_request)

        changed_test_user = User.objects.get(pk=self.test_user.id)

        self.assertEqual(changed_test_user.username, self._new_username)

        empty_field_change_request = self.request_factory.post("change-account-field", data={})
        empty_field_change_request.user = self.test_user

        uncorrect_field_change_request = self.request_factory.post("change-account-field",
                                                                   data={"username": "$# %-0 ~"})
        uncorrect_field_change_request.user = self.test_user

        self.assertEqual(
            type(ChangeAccountDataView.as_view()(empty_field_change_request)), HttpResponseRedirect
        )
        self.assertEqual(
            type(ChangeAccountDataView.as_view()(uncorrect_field_change_request)), HttpResponseRedirect
        )


class ResetUserPasswordViewTestCase(tests_presets.BaseSingleUserTestCase):
    request_factory: RequestFactory
    test_user: User

    def test_get(self):
        reset_password_view = ResetUserPasswordView.as_view()
        reset_password_request = self.request_factory.get("account_change_password")
        reset_password_request.user = self.test_user
        self.assertEqual(
            type(reset_password_view(reset_password_request).context_data["view"]),
            AllauthPasswordResetView
        )
        reset_password_request.user = AnonymousUser()
        self.assertEqual(
            type(reset_password_view(reset_password_request).context_data["view"]),
            ResetUserPasswordView
        )


class RedirectToAccountInfoViewTestCase(tests_presets.BaseSingleUserTestCase):
    def test_get_redirect_url(self):
        redirect_to_account_info_request = self.request_factory.get(reverse("account_email"))
        redirect_to_account_info_request.user = self.test_user

        self.assertTrue(
            tests_utils.response_is_redirect(RedirectToAccountInfoView.as_view()(redirect_to_account_info_request))
        )

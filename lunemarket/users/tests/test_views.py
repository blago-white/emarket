from allauth.account.views import PasswordResetView as AllauthPasswordResetView

from django.http.response import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.template.response import TemplateResponse

from products.models.models import Phones, Category

from . import *

from ..models.models import UserProfile, Notifications
from ..forms import RegisterUserForm
from ..views import (BaseAccountView,
                     LoginUserView,
                     UserPasswordChangeView,
                     AccountInfoView,
                     AccountProductsView,
                     AccountNotificationsView,
                     AccountNotificationDeleteView,
                     ChangeAccountDataView,
                     ResetUserPasswordView,
                     RedirectToAccountInfoView)


class _BaseViewTestCaseWithRequests(TestCase):
    _request_factory = RequestFactory()


class _BaseSingleUserTestCase(_BaseViewTestCaseWithRequests):
    def setUp(self) -> None:
        self._test_user = User(username=TEST_USER_DEFAULT_USERNAME, password=TEST_USER_DEFAULT_PASSWORD)
        self._test_user.save()


class _BaseTwinUsersTestCase(_BaseViewTestCaseWithRequests):
    def setUp(self) -> None:
        self._test_users = dict(
            user1=User(username=TEST_USER_DEFAULT_USERNAME, password=TEST_USER_DEFAULT_PASSWORD),
            user2=User(username=TEST_SECOND_USER_DEFAULT_USERNAME, password=TEST_USER_DEFAULT_PASSWORD),
        )
        for testuser in self._test_users.values():
            testuser.save()


class _BaseNotificationsTestCase(_BaseSingleUserTestCase):
    def _create_notifications_for_user(self, test_user: User) -> None:
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


class UserPasswordChangeViewTestCase(_BaseSingleUserTestCase):
    _request_factory: RequestFactory

    def test_get_context_data(self):
        request = self._request_factory.get(reverse("account_change_password"))
        request.user = self._test_user

        change_password_response = UserPasswordChangeView.as_view()(request)

        for field_name in change_password_response.context_data["form"].fields:
            self.assertFalse(
                "placeholder" in change_password_response.context_data["form"].fields[field_name].widget.attrs.keys()
            )


class AccountInfoViewTestCase(_BaseTwinUsersTestCase):
    _request_factory: RequestFactory
    _test_form_error = "testerror-errorfield"

    def test_get_object(self):
        self._test_account_info()
        self._test_account_info_form_errors()

    def _test_account_info_form_errors(self):
        self_account_info_request_with_error = self._get_test_self_account_info_request_with_form_error(
            test_user=self._test_users.get("user1"), error=self._test_form_error
        )

        account_info_form_error_response = AccountInfoView.as_view()(
            self_account_info_request_with_error,
            pk=self._test_users.get("user1").id,
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
        self_account_info_request = self._get_test_account_info_request(test_user="user1")

        self.assertEqual(
            type(AccountInfoView.as_view()(
                    self_account_info_request, pk=self._test_users.get("user1").id
                ).context_data["object"]
                 ),
            User
        )

        self._create_test_user_profile(test_user=self._test_users.get("user1"))

        self.assertEqual(
            type(AccountInfoView.as_view()(
                self_account_info_request, pk=self._test_users.get("user1").id
            ).context_data["object"]),
            UserProfile
        )

        stranger_account_info_request = self._get_test_account_info_request(
            test_user="user1",
            account_info_pk=self._test_users.get("user2").id
        )

        stranger_account_info_response = AccountInfoView.as_view()(
            stranger_account_info_request, pk=self._test_users.get("user2").id
        )
        self.assertFalse(stranger_account_info_response.context_data.get("is_self_account"))
        self.assertEqual(type(stranger_account_info_response.context_data["object"]), User)

    def _create_test_user_profile(self, test_user: User):
        test_userprofile = UserProfile(user=test_user)
        test_userprofile.save()

    def _get_test_self_account_info_request_with_form_error(self, test_user: int, error: str) -> WSGIRequest:
        test_self_account_info_request = self._request_factory.get(
            reverse("account-info", kwargs={"pk": test_user.id}) + "?error=" + error
        )

        test_self_account_info_request.user = test_user

        return test_self_account_info_request

    def _get_test_account_info_request(self, test_user: str, account_info_pk: int = None) -> WSGIRequest:
        request = self._request_factory.get(
            reverse("account-info", kwargs={"pk": account_info_pk or self._test_users.get(test_user).id})
        )

        request.user = self._test_users.get(test_user)

        return request


class AccountProductsViewTestCase(_BaseTwinUsersTestCase):
    _request_factory: RequestFactory
    _test_users: dict[str, User]

    def test_get_queryset(self):
        self._test_get_query_set_stranger_user()

    def _test_get_query_set_stranger_user(self):
        request = self._request_factory.get(reverse("account-products", kwargs={"pk": self._test_users["user1"].id}))
        request.user = self._test_users["user1"]

        self._create_test_phones_for_user(test_user=self._test_users["user1"])

        self.assertEqual(
            AccountProductsView.as_view()(request, pk=self._test_users["user1"].id).context_data["items"].count(),
            2
        )

        request.user = self._test_users["user2"]

        self.assertEqual(
            AccountProductsView.as_view()(request, pk=self._test_users["user1"].id).context_data["items"].count(),
            1
        )

    def _create_test_phones_for_user(self, test_user: User) -> None:
        test_categories = self._create_test_categories_for_user()
        test_phone_fields = _get_test_phone_fields(
            category=test_categories[0],
            author=test_user
        )

        Phones(**test_phone_fields).save()

        test_phone_fields["products_count"] = 10
        test_phone_fields["title"] += "-second"

        Phones(**test_phone_fields).save()

    def _create_test_categories_for_user(self) -> tuple[Category]:
        test_category = Category(
            title="category",
            photo="test-photo.jpg"
        )
        test_category.save()

        return test_category,


class AccountNotificationsViewTestCase(_BaseNotificationsTestCase):
    _request_factory: RequestFactory
    _test_user: User

    def test_get_context_data(self):
        request = self._request_factory.get(reverse("account-notifications"))
        request.user = self._test_user

        super()._create_notifications_for_user(test_user=self._test_user)

        notifications_response = AccountNotificationsView.as_view()(request)
        self.assertEqual(notifications_response.context_data["notifications"].count(), 1)
        self.assertTrue(notifications_response.context_data["is_self_account"])


class AccountNotificationDeleteViewTestCase(_BaseNotificationsTestCase):
    _request_factory: RequestFactory
    _test_user: User

    def test_get_object(self):
        super()._create_notifications_for_user(test_user=self._test_user)
        test_notification_id = Notifications.objects.all().values("id")[0]["id"]

        notification_delete_view = AccountNotificationDeleteView()
        notification_delete_view.kwargs = {"pk": test_notification_id}

        self.assertEqual(notification_delete_view.get_object(),
                         Notifications.objects.get(pk=test_notification_id))


class ChangeAccountDataViewTestCase(_BaseSingleUserTestCase):
    _new_username = "testusernameChanged"
    _request_factory: RequestFactory
    _test_user: User

    def test_post(self):
        change_username_field_request = self._request_factory.post("change-account-field",
                                                                   data={"username": self._new_username})
        change_username_field_request.user = self._test_user
        ChangeAccountDataView.as_view()(change_username_field_request)

        changed_test_user = User.objects.get(pk=self._test_user.id)

        self.assertEqual(changed_test_user.username, self._new_username)

        empty_field_change_request = self._request_factory.post("change-account-field", data={})
        empty_field_change_request.user = self._test_user

        uncorrect_field_change_request = self._request_factory.post("change-account-field",
                                                                    data={"username": "$# %-0 ~"})
        uncorrect_field_change_request.user = self._test_user

        self.assertEqual(
            type(ChangeAccountDataView.as_view()(empty_field_change_request)), HttpResponseRedirect
        )
        self.assertEqual(
            type(ChangeAccountDataView.as_view()(uncorrect_field_change_request)), HttpResponseRedirect
        )


class ResetUserPasswordViewTestCase(_BaseSingleUserTestCase):
    _request_factory: RequestFactory
    _test_user: User

    def test_get(self):
        reset_password_view = ResetUserPasswordView.as_view()
        reset_password_request = self._request_factory.get("account_change_password")
        reset_password_request.user = self._test_user
        self.assertEqual(
            type(reset_password_view(reset_password_request).context_data["view"]),
            AllauthPasswordResetView
        )
        reset_password_request.user = AnonymousUser()
        self.assertEqual(
            type(reset_password_view(reset_password_request).context_data["view"]),
            ResetUserPasswordView
        )


class RedirectToAccountInfoViewTestCase(_BaseSingleUserTestCase):
    def test_get_redirect_url(self):
        redirect_to_account_info_request = self._request_factory.get(reverse("account_email"))
        redirect_to_account_info_request.user = self._test_user

        self.assertEqual(
            RedirectToAccountInfoView.as_view()(redirect_to_account_info_request).status_code // 100,
            3
        )


def _get_test_phone_fields(category: Category, author: User) -> dict:
    return {
        "title": "test-phone",
        "category": category,
        "photo": "test-photo.jpg",
        "price": 100,
        "views": 0,
        "products_count": 0,
        "author": author,
        "color": "#222222",
        "stortage": 1
    }

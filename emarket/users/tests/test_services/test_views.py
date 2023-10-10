from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.test import TestCase

from emarket.testsutils import tests_presets

from users.services import views, urls
from users.utils.profile_errors import username_errors


class ConfirmUserEmailTestCase(tests_presets.BaseSingleUserTestCase):
    _EMAIL_VERIFICATION_FAIL_URL = reverse("change-account-field")
    _EMAIL_VERIFICATION_FAIL_URL_WITH_ARGS = urls.get_url_with_args(
        url=_EMAIL_VERIFICATION_FAIL_URL, error=""
    )

    def test_confirm_user_email(self):
        confirm_email_try_response = views.confirm_user_email(
            request=self._get_test_change_profile_request(),
            email=self.test_user.email
        )

        self.assertEqual(confirm_email_try_response.status_code, 302)
        self.assertTrue(
            self._EMAIL_VERIFICATION_FAIL_URL_WITH_ARGS in confirm_email_try_response.url
        )

    def _get_test_change_profile_request(self) -> HttpRequest:
        return self.get_request_with_test_user(request_method=self.request_factory.post,
                                               path=reverse("change-account-field"),
                                               email=self.test_user.email)


class GetUsernameErrorCodeTestCase(TestCase):
    _TEST_PROFILE_ERROR = username_errors.UncorrectUsernameError

    def test_get_username_error_code(self):
        self.assertEqual(views.get_username_error_code(
            validation_error=self.get_test_relevant_validation_error(),
            field_name=self._TEST_PROFILE_ERROR.field
        ), self._TEST_PROFILE_ERROR.code)

        self.assertEqual(views.get_username_error_code(
            validation_error=self.get_test_irrelevant_validation_error(),
            field_name=self._TEST_PROFILE_ERROR.field
        ), username_errors.UnexpectedUsernameError.code)

        self.assertRaises(AttributeError, views.get_username_error_code,
                          validation_error=ValidationError(message=self._TEST_PROFILE_ERROR.message),
                          field_name=self._TEST_PROFILE_ERROR.field)

        self.assertRaises(KeyError, views.get_username_error_code,
                          validation_error=self.get_test_relevant_validation_error(),
                          field_name=reversed(self._TEST_PROFILE_ERROR.field))

    def get_test_relevant_validation_error(self):
        return ValidationError(
            message={self._TEST_PROFILE_ERROR.field: self._TEST_PROFILE_ERROR.message}
        )

    def get_test_irrelevant_validation_error(self):
        return ValidationError(
            message={self._TEST_PROFILE_ERROR.field: username_errors.UnexpectedUsernameError.message}
        )

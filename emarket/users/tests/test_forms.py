from django.core.exceptions import ValidationError
from django.test import TestCase
from emarket.testsutils.tests_utils import create_test_user

from . import *
from ..forms import RegisterUserForm


class RegisterUserFormTestCase(TestCase):
    _test_register_user_form = RegisterUserForm(
        data={
            "email": TEST_USER_DEFAULT_EMAIL,
            "password1": TEST_USER_DEFAULT_PASSWORD,
            "password2": TEST_USER_DEFAULT_PASSWORD
        }
    )

    def test_clean_email(self):
        self._test_register_user_form.full_clean()

        self.assertEqual(self._test_register_user_form.clean_email(), TEST_USER_DEFAULT_EMAIL)
        create_test_user()

        with self.assertRaises(ValidationError):
            self._test_register_user_form.clean_email()

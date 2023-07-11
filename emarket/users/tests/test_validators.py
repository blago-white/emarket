from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import validators


class ValidatorsTestCase(TestCase):
    _test_usernames_too_short = ("Ts", "")
    _test_usernames_too_long = ("T"*100, "T"*26)
    _test_usernames_not_correct_letters = ("Robert_", "Robert!", "%Robert", "1Robert", "@@@")

    _test_usernames_correct_length_short = ("Rob", "Anna")
    _test_usernames_correct_length_long = ("T"*25, )
    _test_usernames_correct_letters = ("Robert", "ROBERT", "robert", "--RoBeRt--", "-Robert-")

    def test_username_min_length_validator(self) -> None:
        for too_short_username in self._test_usernames_too_short:
            with self.assertRaises(ValidationError):
                validators.username_min_length_validator(value=too_short_username)

        for correct_short_name in self._test_usernames_correct_length_short:
            validators.username_min_length_validator(value=correct_short_name)

    def test_username_max_length_validator(self) -> None:
        for too_long_username in self._test_usernames_too_long:
            with self.assertRaises(ValidationError):
                validators.username_max_length_validator(value=too_long_username)

        for correct_long_name in self._test_usernames_correct_length_long:
            validators.username_max_length_validator(value=correct_long_name)

    def test_username_letters_validator(self) -> None:
        for not_correct_username in self._test_usernames_not_correct_letters:
            with self.assertRaises(ValidationError):
                validators.username_letters_validator(value=not_correct_username)

        for correct_username in self._test_usernames_correct_letters:
            validators.username_letters_validator(value=correct_username)

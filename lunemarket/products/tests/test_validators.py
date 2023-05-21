from django.core.exceptions import ValidationError
from django.test import TestCase

from products import validators


class ValidatorsTestCase(TestCase):
    _test_category_names_uncorrect = (
        "Phones",
        "PHONES",
        "Phones" * 20,
        "phones-phones"
    )
    _test_card_names_uncorrect = (
        "Phones-",
        "Телефон"
    )
    _test_category_names_correct = (
        "phones",
        "phones " * 2
    )
    _test_card_names_correct = (
        "Phones",
        "Phone 11"
    )

    def test_category_title_validator(self) -> None:
        for uncorrect_category_name in self._test_category_names_uncorrect:
            with self.assertRaises(ValidationError):
                validators.category_title_validator(value=uncorrect_category_name)

        for correct_category_name in self._test_category_names_correct:
            validators.category_title_validator(value=correct_category_name)

    def test_card_title_validator(self) -> None:
        for uncorrect_card_name in self._test_card_names_uncorrect:
            with self.assertRaises(ValidationError):
                validators.card_title_validator(value=uncorrect_card_name)

        for correct_card_name in self._test_card_names_correct:
            validators.card_title_validator(value=correct_card_name)

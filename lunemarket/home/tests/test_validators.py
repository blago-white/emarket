from django.core.exceptions import ValidationError
from django.test import TestCase

from lunemarket.products.validators import category_title_validator


class ValidatorsTestCase(TestCase):
    _test_category_names_uncorrect = (
        "Phones",
        "PHONES",
        "phones1",
        "Phones" * 20,
        "phones-phones"
    )
    _test_category_names_correct = (
        "phones",
        "phones " * 2
    )

    def test_category_name_validator(self) -> None:
        for uncorrect_category_name in self._test_category_names_uncorrect:
            with self.assertRaises(ValidationError):
                category_title_validator(value=uncorrect_category_name)

        for correct_category_name in self._test_category_names_correct:
            category_title_validator(value=correct_category_name)

from django.test import TestCase

from emarket.testsutils.tests_presets import BaseSingleUserTestCase
from emarket.testsutils import tests_utils

from products.models.models import Phone

from ..models import ShoppingBasket


class FiltersTestCase(BaseSingleUserTestCase):
    _test_product: Phone
    _test_file_path = "photos/test-photo.png"

    def setUp(self) -> None:
        super().setUp()
        self._test_product = tests_utils.create_test_product(test_user=self.test_user)

    def test_str(self):
        test_basket = ShoppingBasket(user=self.test_user, product=self._test_product)

        self.assertEqual(str(test_basket), f"{self.test_user.username}'s {self._test_product.readable_title()}")

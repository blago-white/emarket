import random

from django.test import TestCase

from emarket import config
from emarket.testsutils import tests_presets, tests_utils
from products.models.models import Phone, BaseProduct
from products.services import models


class ModelsServicesTestCase(tests_presets.BaseSingleUserTestCase):
    def test_get_max_product_price(self):
        self.assertIsNone(models.get_max_product_price(Phone, price_field_name="price"))

        self._create_test_products()

        self.assertEqual(
            models.get_max_product_price(Phone, price_field_name="price"), max(self._test_prices)
        )

        with self.assertRaises(AttributeError):
            models.get_max_product_price(products=BaseProduct, price_field_name="")

    def _create_test_products(self):
        self._test_prices = _get_random_prices()

        self._test_category = tests_utils.create_default_test_category()
        self._test_products = [
            tests_utils.create_test_product(
                test_user=self.test_user,
                test_category=self._test_category,
                price=random_price
            ) for random_price in self._test_prices
        ]


def _get_random_prices() -> tuple[int]:
    return [random.randint(0, config.MAX_PRODUCT_PRICE_USD) for _ in range(10)]

from django.test import TestCase

from emarket.testsutils.tests_presets import BaseSingleUserTestCase
from emarket.testsutils import tests_utils

from products.models import models
from products.models import utils


class ModelsUtilitsTestCase(BaseSingleUserTestCase):
    _test_product: models.Phone

    def setUp(self) -> None:
        super().setUp()
        self._test_product = tests_utils.create_test_product(test_user=self.test_user)

    def test_get_image_path(self) -> None:
        image_path = utils.get_image_path(self=models.Category(), filename="test_file.png")
        self.assertEqual(image_path.split("/")[0], "category")
        self.assertEqual(image_path.split("/")[-1].split(".")[-1], "png")
        (self.assertFalse if " " in image_path.split("/")[-1] else self.assertTrue)(expr="Spaces in dirname")

    def test_decrease_phones_count(self):
        self._test_decrease_phones_count()
        self._test_decrease_phones_count_exception()

    def _test_decrease_phones_count(self):
        old_products_count = self._test_product.products_count

        models_utils.decrease_phones_count(phone=self._test_product)

        self.assertEqual(old_products_count - 1,
                         models.Phone.objects.get(pk=self._test_product.pk).products_count)

    def _test_decrease_phones_count_exception(self):
        with self.assertRaises(ValueError):
            utils.decrease_phones_count(phone=models.Phone.objects.get(pk=self._test_product.pk))

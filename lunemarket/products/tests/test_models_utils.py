from django.core.exceptions import ValidationError
from django.test import TestCase

from products.models import models_utils
from products.models import models


class ModelsUtilitsTestCase(TestCase):
    def test_get_image_path(self) -> None:
        image_path = models_utils.get_image_path(self=models.Categories(), filename="test_file.png")
        self.assertEqual(image_path.split("/")[0], "categories")
        self.assertEqual(image_path.split("/")[-1].split(".")[-1], "png")
        (self.assertFalse if " " in image_path.split("/")[-1] else self.assertTrue)(expr="Spaces in dirname")

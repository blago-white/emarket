from django.core.exceptions import ValidationError
from emarket.testsutils import tests_utils
from emarket.testsutils.tests_presets import BaseSingleUserTestCase, TEST_PHONE_DEFAULT_FIELDS

from ..filters import dashes_to_spaces
from ..models.models import Phone, Category


class PhonesModelTestCase(BaseSingleUserTestCase):
    _test_product: Phone
    _test_category: Category

    def setUp(self) -> None:
        super().setUp()
        self._test_category = tests_utils.create_default_test_category()
        self._test_product = tests_utils.create_test_product(test_user=self.test_user, test_category=self._test_category)

    def test_readable_title(self):
        self.assertEqual(self._test_product.readable_title(), dashes_to_spaces(self._test_product.title))

    def test_delete(self):
        self._add_second_test_product().delete()
        self.assertEqual(Phone.objects.filter(category=self._test_category).count(), 1)
        self._test_product.delete()
        self.assertEqual(Category.objects.all().count(), 0)

    def test_str(self):
        self.assertEqual(str(self._test_product), self._test_product.title)

    def _add_second_test_product(self) -> Phone:
        second_test_product_fields = TEST_PHONE_DEFAULT_FIELDS.copy()

        second_test_product_fields["category"] = self._test_category
        second_test_product_fields["author"] = self.test_user
        second_test_product_fields["title"] = self._test_product.title + "-second"

        return tests_utils.create_test_phone(fields=second_test_product_fields)


class CategoryModelTestCase(BaseSingleUserTestCase):
    _test_parent_category: Category
    _test_child_category: Category
    _CHILD_CATEGORY_FIELDS = dict(title="child-test-category",
                                  parent=None,
                                  photo="test-photo.jpg")
    _PARENT_CATEGORY_FIELDS = dict(title="parentcategory", photo="test-photo.jpg")
    
    def test_clean(self):
        test_parent_category_invalid_fields = self._PARENT_CATEGORY_FIELDS.copy()
        test_parent_category_invalid_fields["title"] = self._CHILD_CATEGORY_FIELDS["title"]

        with self.assertRaises(ValidationError):
            Category(**test_parent_category_invalid_fields).clean()



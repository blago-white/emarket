from django.test import TestCase
from ..views_utils import convert_category_filters_to_product_filters


class ViewsUtilsTestCase(TestCase):
    _test_categories_query_filters = {"phone__count": 10, "phone__price__min": 500}
    _test_phones_query_filters = {"count": 10, "price__min": 500}

    def test_convert_category_filters_to_product_filters(self):
        convert_category_filters_to_product_filters(self._test_categories_query_filters),

        self.assertEqual(
            self._test_categories_query_filters,
            self._test_phones_query_filters
        )

        self.assertEqual({}, {})

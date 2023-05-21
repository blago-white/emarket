from django.test import TestCase
from products.filters import get_categories_batches


class FiltersTestCase(TestCase):
    def test_get_categories_batches(self) -> None:
        test_categories_query_sets = list()
        test_categories_query_sets.append(["tablets", "routers", "phones",
                                           "mouses", "monitors", "laptops",
                                           "keyboards", "headphones", "cameras"])
        test_categories_query_sets.append(test_categories_query_sets[0] * 2)

        test_batches = (get_categories_batches(test_categories_query_sets[0]),
                        get_categories_batches(test_categories_query_sets[1]))

        self.assertEqual(test_batches,
                         ([test_categories_query_sets[0]],
                          [test_categories_query_sets[0], test_categories_query_sets[0]])
                         )

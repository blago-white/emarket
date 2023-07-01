from django.test import TestCase

from products.filters import *


class FiltersTestCase(TestCase):
    maxDiff = None

    _test_categories_simple_query_set = ("phones", ) * 9
    _test_categories_duplicated_query_set = _test_categories_simple_query_set * 2
    _test_spaced_prompts = ("Iphone 11", "I p h o n e 1  1", "Iphone11", "  ", None)
    _test_dashed_prompts = [(prompt.replace(" ", "-") if prompt else prompt) for prompt in _test_spaced_prompts]
    _test_get_prices_range_values = ((1111, [0, 1000, 1111]),
                                     (1, [0, 1]),
                                     (2000, [0, 1000, 2000]))
    _test_get_url_arg_from_bool_values = (((True, "price"), "price"),
                                          ((False, "price"), ""))
    _test_invert_sorting_values = (("0", "1"), ("1", "0"), ("test", "test"))
    _test_compile_url_args_for_pagination_values = ((("0", True, 100), "&price=0&filters&min=100"),
                                                    ((None, None, None), ""),
                                                    ((None, True, None), "&filters"),
                                                    ((None, True, 100), "&filters&min=100"))
    _test_get_ordering_field_from_url_arg_values = ((("0", "price"), "price"),
                                                    (("1", "price"), "-price"),
                                                    (("test_not_int_arg", "price"), "price"))
    _test_get_url_arg_from_ordering_field_values = (("price", 0), ("-price", 1))

    def test_get_categories_batches(self) -> None:
        test_batches = (get_categories_batches(self._test_categories_simple_query_set),
                        get_categories_batches(self._test_categories_duplicated_query_set))

        self.assertEqual(test_batches,
                         ([self._test_categories_simple_query_set],
                          [self._test_categories_simple_query_set]*2)
                         )

    def test_spaces_to_dashes(self) -> None:
        for prompt_idx, spaced_prompt in enumerate(self._test_spaced_prompts):
            self.assertEqual(spaces_to_dashes(spaced_prompt), self._test_dashed_prompts[prompt_idx])

    def test_dashes_to_spaces(self) -> None:
        for prompt_idx, dashed_prompt in enumerate(self._test_dashed_prompts):
            self.assertEqual(dashes_to_spaces(dashed_prompt), self._test_spaced_prompts[prompt_idx])

    def test_get_prices_range(self) -> None:
        for max_price, result in self._test_get_prices_range_values:
            self.assertEqual(get_prices_range(max_price), result)

    def test_get_url_arg_from_bool(self) -> None:
        for inputs, result in self._test_get_url_arg_from_bool_values:
            self.assertEqual(get_url_arg_from_bool(*inputs), result)

    def test_invert_sorting(self) -> None:
        for sorting, result in self._test_invert_sorting_values:
            self.assertEqual(invert_sorting(sorting), result)

    def test_compile_url_args_for_pagination(self) -> None:
        for inputs, result in self._test_compile_url_args_for_pagination_values:
            self.assertEqual(compile_url_args_for_pagination(*inputs), result)

    def test_get_ordering_field_from_url_arg(self) -> None:
        for inputs, result in self._test_get_ordering_field_from_url_arg_values:
            self.assertEqual(get_ordering_field_from_url_arg(*inputs), result)

    def test_get_url_arg_from_ordering_field(self) -> None:
        for field, result in self._test_get_url_arg_from_ordering_field_values:
            self.assertEqual(get_url_arg_from_ordering_field(field), result)

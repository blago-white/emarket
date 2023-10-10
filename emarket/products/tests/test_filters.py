from django.test import TestCase

from products.filters import *


class FiltersTestCase(TestCase):
    maxDiff = None

    _test_spaced_prompts = ("Iphone 11", "I p h o n e 1  1", "Iphone11", "  ", None)
    _test_dashed_prompts = [(prompt.replace(" ", "-") if prompt else prompt) for prompt in _test_spaced_prompts]

    def test_get_categories_batches(self) -> None:
        test_categories_simple_query_set = ("phones",) * 9
        test_categories_duplicated_query_set = test_categories_simple_query_set * 2

        test_batches = (get_categories_batches(test_categories_simple_query_set),
                        get_categories_batches(test_categories_duplicated_query_set))

        self.assertEqual(test_batches,
                         ([test_categories_simple_query_set],
                          [test_categories_simple_query_set] * 2)
                         )

    def test_spaces_to_dashes(self) -> None:
        for prompt_idx, spaced_prompt in enumerate(self._test_spaced_prompts):
            self.assertEqual(spaces_to_dashes(spaced_prompt), self._test_dashed_prompts[prompt_idx])

    def test_dashes_to_spaces(self) -> None:
        for prompt_idx, dashed_prompt in enumerate(self._test_dashed_prompts):
            self.assertEqual(dashes_to_spaces(dashed_prompt), self._test_spaced_prompts[prompt_idx])

    def test_get_prices_range(self) -> None:
        test_prices_range_values = ((1111, [0, 300, 600, 900, 1111]),
                                    (1, [0, 1]),
                                    (2000, [0, 1000, 2000]))

        for max_price, result in test_prices_range_values:
            self.assertEqual(get_prices_range(max_price), result)

    def test_get_url_arg_from_bool(self) -> None:
        test_get_url_arg_from_bool_values = (((True, "price"), "price"),
                                             ((False, "price"), ""))

        for inputs, result in test_get_url_arg_from_bool_values:
            self.assertEqual(get_url_arg_from_bool(*inputs), result)

    def test_invert_sorting(self) -> None:
        test_invert_sorting_values = (("0", "1"), ("1", "0"), ("test", "test"))

        for sorting, result in test_invert_sorting_values:
            self.assertEqual(invert_sorting(sorting), result)

    def test_underlines_to_spaces(self):
        test_underlined_string = "some_string"
        test_spaced_string = "some string"

        self.assertEqual(underlines_to_spaces(test_underlined_string), test_spaced_string)
        self.assertEqual(underlines_to_spaces(""), "")
        self.assertEqual(underlines_to_spaces("__"), "  ")

    def test_round_(self):
        test_float_numbers = (1.11, 3.333, 4.5, 5.9)
        test_rounded_numbers = (1, 3.3, 4, 5.900)
        test_round_factors = (0, 1, 0, 3)

        for idx, test_float_number in enumerate(test_float_numbers):
            self.assertEqual(round_(test_float_number, test_round_factors[idx]),
                             test_rounded_numbers[idx])

        self.assertEqual(round_("test", 1), "test")

    def test_truncate(self):
        self.assertEqual(truncate("test long string", 4), "test")
        self.assertEqual(truncate("test", 10), "test")
        self.assertEqual(truncate("", 4), "")

    def test_get_element_by_index(self):
        test_sequence = [idx for idx in range(4)]

        self.assertEqual(get_element_by_index(sequence=test_sequence, idx=0), test_sequence[0])
        self.assertEqual(get_element_by_index(sequence=test_sequence, idx=-1), test_sequence[-1])

        with self.assertRaises(IndexError):
            get_element_by_index(sequence=test_sequence, idx=5)



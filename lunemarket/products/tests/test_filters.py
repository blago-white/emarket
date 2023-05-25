from django.test import TestCase
from products.filters import get_categories_batches, spaces_to_dashes, dashes_to_spaces


class FiltersTestCase(TestCase):
    maxDiff = None
    _test_categories_simple_query_set = ["phones"] * 9
    _test_categories_duplicated_query_set = _test_categories_simple_query_set * 2
    _test_spaced_prompts = ["Iphone 11", "I p h o n e 1  1", "Iphone11", "  ", None]
    _test_dashed_prompts = [(prompt.replace(" ", "-") if prompt else prompt) for prompt in _test_spaced_prompts]

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

from django.test import TestCase
from ..filters import *


class FiltersTestCase(TestCase):
    maxDiff = None
    _test_wrap_stmts = ((0, ("", )),
                        (1, ("l"*18, "l")),
                        (2, ("l"*19, "l"*36)))
    _test_enumerate_sequences = ((1, 2, 3),
                                 {1, 2, 3},
                                 [1, 2, 3],
                                 [])

    def test_wrap(self) -> None:
        for goal_length, stmts in self._test_wrap_stmts:
            for stmt in stmts:
                self.assertEqual(len(wrap(stmt)), goal_length)

    def test_enumerate_(self) -> None:
        for test_sequence in self._test_enumerate_sequences:
            self.assertEqual(tuple(enumerate_(test_sequence)), tuple(enumerate(test_sequence)))

    def test_get_title_theme(self) -> None:
        self.assertEqual(get_title_theme(name="inf"), "info")
        self.assertEqual(get_title_theme(name="pur"), "purchase")
        self.assertEqual(get_title_theme(name="none"), None)

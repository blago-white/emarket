from django.test import TestCase

from users.sections import BaseAccountSection


class BaseAccountSectionTestCase(TestCase):
    _TEST_SECTION_NAME = "test"

    def test_section_name(self):
        test_section = self._get_test_section()

        self.assertEqual(str(test_section), self._TEST_SECTION_NAME)
        self.assertEqual(test_section.__repr__(), self._TEST_SECTION_NAME)
        self.assertEqual(test_section.section_name, self._TEST_SECTION_NAME)


    def _get_test_section(self) -> BaseAccountSection:
        class _TestAccountSection(BaseAccountSection):
            section_name = self._TEST_SECTION_NAME

        return _TestAccountSection()

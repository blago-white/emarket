from django.test import TestCase
from ..filters import get_media_path


class FiltersTestCase(TestCase):
    _test_file_path = "photos/test-photo.png"

    def test_get_media_path(self):
        self.assertEqual(get_media_path(self._test_file_path), "../uploads/"+self._test_file_path)
        self.assertEqual(get_media_path(""), "../uploads/")

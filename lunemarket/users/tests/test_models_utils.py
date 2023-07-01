from django.test import TestCase
from django.contrib.auth.models import User

from ..models.models import UserProfile
from ..models.models_utils import get_image_path


class ModelsUtilsTestCase(TestCase):
    _test_profile: UserProfile = UserProfile(user=User(id=1, username="testusername"), avatar="")
    _test_file_name: str = "test-file-name.png"

    def test_get_image_path(self) -> None:
        self.assertEqual(get_image_path(self=self._test_profile, filename=self._test_file_name),
                         f"avatars/{self._test_profile.user.id}.{self._test_file_name.split('.')[-1]}")

        with self.assertRaises(AttributeError):
            get_image_path(self=int(), filename=int())

        with self.assertRaises(AttributeError):
            get_image_path(self=self._test_profile, filename=int())

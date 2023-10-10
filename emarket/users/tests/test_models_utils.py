from django.core.exceptions import ValidationError

from emarket import config
from emarket.testsutils.tests_presets import BaseSingleUserTestCase

from ..models.models import UserProfile
from ..models import utils


class ModelsUtilsTestCase(BaseSingleUserTestCase):
    _test_profile: UserProfile
    _test_file_name: str = "test-file-name.png"

    def setUp(self) -> None:
        super(ModelsUtilsTestCase, self).setUp()
        self._test_profile = UserProfile(user=self.test_user)

    def test_validate_avatar_resolution(self) -> None:
        with self.assertRaises(ValidationError):
            utils.validate_avatar_resolution(photo_width=config.MINIMUM_PHOTO_RESOLUTION_WIDTH-1,
                                             photo_height=config.MINIMUM_PHOTO_RESOLUTION_HEIGHT-1)

        with self.assertRaises(ValidationError):
            utils.validate_avatar_resolution(photo_width=config.MAXIMUM_PHOTO_RESOLUTION_WIDTH+1,
                                             photo_height=config.MAXIMUM_PHOTO_RESOLUTION_HEIGHT+1)

        with self.assertRaises(ValidationError):
            utils.validate_avatar_resolution(photo_width=config.MAXIMUM_PHOTO_RESOLUTION_WIDTH,
                                             photo_height=config.MINIMUM_PHOTO_RESOLUTION_HEIGHT)

        self.assertIsNone(utils.validate_avatar_resolution(photo_width=config.MAXIMUM_PHOTO_RESOLUTION_WIDTH,
                                                           photo_height=config.MAXIMUM_PHOTO_RESOLUTION_HEIGHT))

    def test_get_image_path(self) -> None:
        self.assertEqual(utils.get_image_path(self=self._test_profile),
                         f"avatars/{self._test_profile.user.id}.{self._test_file_name.split('.')[-1]}")

        with self.assertRaises(AttributeError):
            utils.get_image_path(self=UserProfile())

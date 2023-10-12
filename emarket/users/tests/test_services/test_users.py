from allauth.socialaccount.models import SocialAccount

from emarket.testsutils import tests_presets
from users.services import users
from users.models.models import UserProfile


class UsersServiceTestCase(tests_presets.BaseSingleUserTestCase):
    _test_user_profile: UserProfile
    _TEST_SOCIALACCOUNT: SocialAccount
    _TEST_AVATAR_NAME: str = "1.png"

    def test_get_user_avatar_url(self):
        self.assertIsNone(users.get_user_avatar_url(user_id=self.test_user.pk))

        self._create_test_empty_userprofile()

        self.assertIsNone(users.get_user_avatar_url(user_id=self.test_user.pk))

        self._add_avatar_for_profile()

        self.assertIsNotNone(users.get_user_avatar_url(user_id=self.test_user.pk))


    def _create_test_empty_userprofile(self):
        self._test_user_profile = UserProfile(user=self.test_user)
        self._test_user_profile.save()

    def _add_avatar_for_profile(self):
        self._test_user_profile.avatar = self._TEST_AVATAR_NAME
        self._test_user_profile.save()

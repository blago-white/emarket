import datetime

from PIL.JpegImagePlugin import JpegImageFile
from django.core.exceptions import ValidationError
from django.conf import settings

from emarket.testsutils.tests_presets import BaseSingleUserTestCase

from ..models.models import Notifications, UserProfile


class NotificationsModelTestCase(BaseSingleUserTestCase):
    def test_str(self) -> None:
        datetime_now = datetime.datetime.now()
        test_notification = Notifications(
            recipient=self.test_user,
            time=datetime_now
        )

        self.assertEqual(str(test_notification), f"{self.test_user.username} - {datetime_now}")

    def test_clean(self) -> None:
        test_notification_sender_is_recipient = Notifications(recipient=self.test_user, sender=self.test_user)
        test_notification_without_sender = Notifications(recipient=self.test_user, theme="pur")

        with self.assertRaises(ValidationError):
            test_notification_sender_is_recipient.clean()

        with self.assertRaises(ValidationError):
            test_notification_without_sender.clean()


class UserProfileModelTestCase(BaseSingleUserTestCase):
    _test_user_profile: UserProfile

    def setUp(self) -> None:
        super().setUp()
        self._create_test_user_profile()

    def test_str(self):
        self.assertEqual(str(self._test_user_profile), f"{self.test_user.username}'s profile")

    def _create_test_user_profile(self):
        self._test_user_profile = UserProfile(user=self.test_user, avatar="")
        self._test_user_profile.save()

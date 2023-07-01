import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from ..models.models import Notifications, UserProfile

_test_user = User(id=1, username="testusername")


class NotificationsModelTestCase(TestCase):
    def test_str(self) -> None:
        datetime_now = datetime.datetime.now()
        test_notification = Notifications(
            recipient=_test_user,
            time=datetime_now
        )

        self.assertEqual(str(test_notification), f"{_test_user.username} - {datetime_now}")

    def test_clean(self) -> None:
        test_notification_sender_is_recipient = Notifications(recipient=_test_user, sender=_test_user)
        test_notification_without_sender = Notifications(recipient=_test_user, theme="pur")

        with self.assertRaises(ValidationError):
            test_notification_sender_is_recipient.clean()

        with self.assertRaises(ValidationError):
            test_notification_without_sender.clean()


class UserProfileModelTestCase(TestCase):
    def test_str(self):
        test_profile = UserProfile(user=_test_user, avatar="")
        self.assertEqual(str(test_profile), f"{_test_user.username}'s profile")

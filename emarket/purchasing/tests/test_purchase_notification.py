from django.contrib.auth.models import User

from emarket.testsutils.tests_presets import BaseTwinUsersTestCase
from emarket.testsutils import tests_utils

from users.models.models import Notifications
from products.models.models import Phone

from ..notifications import purchase_notification
from .. import *


class PurchaseNotificationTestCase(BaseTwinUsersTestCase):
    _test_product: Phone
    _test_owner: User
    _test_purchaser: User

    _FILLED_PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE: str
    _FILLED_PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE: str

    _TEST_PRODUCT_COUNT = 1

    def setUp(self) -> None:
        super().setUp()
        self._test_owner, self._test_purchaser = self.first_test_user, self.second_test_user
        self._create_test_product()
        self._fill_messages_templates()

    def test_notify_about_purchase(self):
        purchase_notification.notify_about_purchase(purchaser=self._test_purchaser,
                                                    owner=self._test_owner,
                                                    product=self._test_product)
        self._test_notifications()

    def _test_notifications(self):
        created_notifications = Notifications.objects.all()
        notification_for_owner: Notifications = Notifications.objects.get(recipient=self._test_owner)
        notification_for_purchaser: Notifications = Notifications.objects.get(recipient=self._test_purchaser)

        self.assertEqual(created_notifications.count(), 2)
        self.assertEqual(notification_for_owner.theme, "pur")
        self.assertEqual(notification_for_purchaser.theme, "inf")

        self.assertEqual(notification_for_owner.text, self._FILLED_PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE)
        self.assertEqual(notification_for_purchaser.text, self._FILLED_PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE)

    def _create_test_product(self):
        self._test_product = tests_utils.create_test_product(test_user=self._test_owner,
                                                             products_count=self._TEST_PRODUCT_COUNT)

    def _fill_messages_templates(self):
        message_template_content = {
            "username": self._test_purchaser.username,
            "usermail": self._test_purchaser.email,
            "productname": self._test_product.readable_title(),
            "price": self._test_product.price
        }

        self._FILLED_PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE = PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE.format(
            **message_template_content,
        )

        message_template_content["username"] = self._test_owner.username
        message_template_content["usermail"] = self._test_owner.email

        self._FILLED_PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE = PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE.format(
            **message_template_content
        )

from lunemarket.lunemarket_tests.tests_presets import BaseSingleUserTestCase
from lunemarket.lunemarket_tests import tests_utils

from users.models.models import Notifications
from products.models.models import Phones

from ..notifications import product_is_over_notification
from products.filters import dashes_to_spaces
from .. import *


class ProductIsOverNotificationTestCase(BaseSingleUserTestCase):
    _test_product: Phones
    _FILLED_PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE: str

    def setUp(self) -> None:
        super().setUp()
        self._test_product = tests_utils.create_test_product(test_user=self.test_user)

        self._FILLED_PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE = PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE.format(
            productname=dashes_to_spaces(self._test_product.title)
        )

    def test_notify_product_is_over(self):
        product_is_over_notification.notify_product_is_over(recipient=self.test_user, product=self._test_product)
        self._test_notifications()

    def _test_notifications(self):
        created_notifications = Notifications.objects.all()

        self.assertEqual(created_notifications.count(), 1)
        self.assertEqual(created_notifications[0].recipient, self.test_user)
        self.assertEqual(created_notifications[0].theme, "inf")
        self.assertEqual(created_notifications[0].text, self._FILLED_PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE)

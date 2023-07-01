from django.contrib.auth.models import User
from products.models.models import Phones
from users.models.models import Notifications
from products.filters import dashes_to_spaces
from . import try_save_notification
from ..emails import send_notification

from purchasing import *

__all__ = ["notify_product_is_over"]


def notify_product_is_over(recipient: User, product: Phones) -> None:
    notification_text = PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE.format(productname=dashes_to_spaces(product.title))
    notification = Notifications(recipient=recipient, text=notification_text, theme="inf")
    try_save_notification(notification=notification)

    _send_product_is_over_email(user=recipient, productname=dashes_to_spaces(product.title))


def _send_product_is_over_email(user: User, productname: Phones):
    message = PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE.format(productname=dashes_to_spaces(productname))
    send_notification(message=message, recipient_mail=user.email)

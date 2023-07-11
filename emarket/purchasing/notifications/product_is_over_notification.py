from django.contrib.auth.models import User
from products.models.models import Phone
from users.models.models import Notifications
from products.filters import dashes_to_spaces
from . import try_save_notification
from ..emails import send_notification

from purchasing import *

__all__ = ["notify_product_is_over"]


def notify_product_is_over(recipient: User, product: Phone) -> None:
    notification_text = PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE.format(productname=product.readable_title())
    notification = Notifications(recipient=recipient, text=notification_text, theme="inf")
    try_save_notification(notification=notification)

    _send_product_is_over_email(user=recipient, productname=product.readable_title())


def _send_product_is_over_email(user: User, productname: Phone):
    message = PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE.format(productname=productname)
    send_notification(message=message, recipient_mail=user.email)

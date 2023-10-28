from django.contrib.auth.models import User

from products.models.models import Phone
from purchasing.emails.templates import (PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE,
                                         PRODUCT_IS_OVER_WARNING_MESSAGE_HTML_TEMPLATE)
from users.models.models import Notifications
from . import try_save_notification
from ..tasks import send_notification

__all__ = ["notify_product_is_over"]


def notify_product_is_over(recipient: User, product: Phone) -> None:
    notification_text = PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE.format(productname=product.readable_title())
    notification = Notifications(recipient=recipient, text=notification_text, theme="inf")
    try_save_notification(notification=notification)

    _send_product_is_over_email(user=recipient, productname=product)


def _send_product_is_over_email(user: User, productname: Phone):
    message = PRODUCT_IS_OVER_WARNING_MESSAGE_HTML_TEMPLATE.format(productid=productname.pk,
                                                                   productname=productname.readable_title())
    send_notification(message=message, recipient_mail=user.email)

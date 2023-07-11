from django.contrib.auth.models import User
from products.models.models import Phone
from users.models.models import Notifications
from . import try_save_notification
from ..emails import EmailPurchaseNotification

from purchasing import *

__all__ = ["notify_about_purchase"]


def notify_about_purchase(purchaser: User, owner: User, product: Phone) -> None:
    _add_purchase_notification_for_owner(purchaser=purchaser,
                                         owner=owner,
                                         product=product)
    _add_purchase_notification_for_purchaser(purchaser=purchaser, owner=owner, product=product)
    _send_purchase_info_email(user=purchaser, product=product)


def _add_purchase_notification_for_purchaser(purchaser: User, owner: User, product: Phone) -> None:
    notification_text = PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE.format(username=owner.username,
                                                                       productname=product.readable_title(),
                                                                       usermail=owner.email,
                                                                       price=product.price)
    notification = Notifications(recipient=purchaser, text=notification_text, theme="inf")
    try_save_notification(notification=notification)


def _add_purchase_notification_for_owner(purchaser: User, owner: User, product: Phone) -> None:
    notification_text = PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE.format(username=purchaser.username,
                                                                   productname=product.readable_title(),
                                                                   usermail=purchaser.email,
                                                                   price=product.price)

    notification = Notifications(recipient=owner, sender=purchaser, text=notification_text, theme="pur")
    try_save_notification(notification=notification)


def _send_purchase_info_email(user: User, product: Phone) -> None:
    email_purchase = EmailPurchaseNotification(purchaser_name=user.username, purchaser_mail=user.email)
    email_purchase.send_notification(product=product)

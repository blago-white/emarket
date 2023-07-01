import django.conf
from django.core.mail import send_mail
from .models import Phones
from . import PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE, PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE

__all__ = ["EmailPurchaseNotification", "send_notification"]


class _BaseEmailNotification:
    def __init__(self, recipient_name: str, recipient_mail: str):
        self._recipient_mail = recipient_mail
        self._recipient_name = recipient_name


class EmailPurchaseNotification(_BaseEmailNotification):
    def __init__(self, purchaser_name: str, purchaser_mail: str):
        super(EmailPurchaseNotification, self).__init__(recipient_name=purchaser_name, recipient_mail=purchaser_mail)

    def send_notification(self, product: Phones) -> None:
        self._send_purchase_message(purchase_message_template=PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE,
                                    product=product,
                                    recipient_mail=product.author.email)
        self._send_purchase_message(purchase_message_template=PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE,
                                    product=product,
                                    recipient_mail=self._recipient_mail)

    def _send_purchase_message(self, purchase_message_template: str, product: Phones, recipient_mail: str) -> None:
        message = purchase_message_template.format(username=self._recipient_name,
                                                   productname=product.title,
                                                   usermail=self._recipient_mail,
                                                   price=product.price)

        send_notification(message=message, recipient_mail=recipient_mail, subject="purchase")


def send_notification(message: str, recipient_mail: str, subject: str = "info") -> None:
    send_mail(subject=subject,
              from_email=django.conf.settings.DEFAULT_FROM_EMAIL,
              message=message,
              recipient_list=[recipient_mail])
